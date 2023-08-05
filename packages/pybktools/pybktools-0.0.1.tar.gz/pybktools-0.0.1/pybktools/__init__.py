# Make this a package

import time, os, re
from base64 import decodestring
import urllib2
from random import randrange
import elementtree.ElementTree as ET

import pybktools

ns_soap ="{http://schemas.xmlsoap.org/soap/envelope/}"
ns_samlp = "{urn:oasis:names:tc:SAML:1.0:protocol}"
ns_samla = "{urn:oasis:names:tc:SAML:1.0:assertion}"
ns_person = "{http://reference.e-government.gv.at/namespace/persondata/20020228#}"
ns_mandate = "{http://reference.e-government.gv.at/namespace/mandates/20040701#}"
ns_bkuSL = "{http://www.buergerkarte.at/namespaces/securitylayer/1.2#}"
ns_dsig = "{http://www.w3.org/2000/09/xmldsig#}"
ns_moa = "{http://reference.e-government.gv.at/namespace/moa/20020822#}"
ns_xhtml = "{http://www.w3.org/1999/xhtml}"

tmpl_dir = pybktools.__path__[0]

class MoaIDAuthException(Exception):
    """A MOA-ID Specific authentication exception"""

def soaptime():
    """Return current time in SOAP format as string"""
    timestr = time.strftime("%Y-%m-%dT%H:%M:%S")
    tz = time.strftime("%z")
    if len(tz) == 5:
        tz = tz[:3] + ':' + tz[3:]
    else:
        tz = ''
    return timestr + tz

def read_person(xml_person):
    """Read person data and return it"""
    d = {}
    d['id'] = xml_person.find(
        ns_person+'Identification').find(
        ns_person+'Value').text
    xml_name = xml_person.find(ns_person+'Name')
    d['forename'] = xml_name.find(ns_person+'GivenName').text
    d['surename'] = xml_name.find(ns_person+'FamilyName').text
    d['birthdate'] = xml_person.find(ns_person+'DateOfBirth').text
    return d

def create_signature_req(xhtmlstr):
        fd = open(os.path.join(tmpl_dir,
            "tmpl/SIGN-CreateXMLSignatureREQUEST.xml"))
        reqstr = fd.read()
        fd.close()
        reqstr = reqstr.replace("REPLACE_WITH_XHTML_CONTENT", xhtmlstr)
        return reqstr

def check_signature_result(xmlbuf):
    """Check signature result for errors and return them, else, return []"""
    xmlres = ET.XML(xmlbuf.encode('UTF-8')) # Hmmm, encode is not very nice...
    errorcode = xmlres.find(ns_bkuSL + 'ErrorCode')
    errorstr = xmlres.find(ns_bkuSL + 'Info')
    if errorcode is not None or errorstr is not None:
        return "%s: %s" % (errorcode.text, errorstr.text)
    return None

def verify_signer(xmlbuf, login_info, sign_verify_url):
    """Verify that the sign info in the XML response == login information"""
    fd = open(os.path.join(tmpl_dir,
        "tmpl/MOA-SP-VerifySignatureRequest.xml"))
    soap_tmpl = fd.read()
    fd.close()
    # Remove surrounding <CreateXMLSignatureResponse> element
    xmlbuf = re.search(
        "CreateXMLSignatureResponse.*?>(.*)</.*:CreateXMLSignatureResponse", 
        xmlbuf, re.S).groups(0)[0] 
    soap_data = soap_tmpl.replace(
        "REPLACE_WITH_SIGNED_XML_DATA", xmlbuf).encode('UTF-8')
    fd = open("/tmp/moa-request.xml", 'w')
    fd.write(soap_data)
    fd.close()
    # FIXME - Put MOA-URL into Configuration
    req = urllib2.Request(url = sign_verify_url,
                          data = soap_data)
    req.add_header('Content-type', 'text/xml')
    req.add_header('SOAPAction', '')
    req.add_header('Cache-Control', 'no-cache')
    req.add_header('Pragma', 'no-cache')
    req.add_header('Connection', 'keep-alive')
    f = urllib2.urlopen(req)

    # Read and interprete result
    result = f.read()
    # Save result
    fd = open("/tmp/moa-result.xml", 'w')
    fd.write(result)
    fd.close()
    xmlres = ET.XML(result) 
    response = xmlres.find(ns_soap+'Body').find(
        ns_moa+'VerifyXMLSignatureResponse')
    if not response:
        return ([1], None)
    # Check signature verification
    signatureCheck = int(response.find(
        ns_moa+'SignatureCheck').find(
            ns_moa+'Code').text)
    signatureManifestCheck = int(response.find(
        ns_moa+'SignatureManifestCheck').find(
            ns_moa+'Code').text)
    certificateCheck = int(response.find(
        ns_moa+'CertificateCheck').find(
            ns_moa+'Code').text)
    if signatureCheck + signatureManifestCheck + certificateCheck != 0:
        return ([0, signatureCheck, signatureManifestCheck, certificateCheck],
                None)
    # Now check that the login/signer is the same
    x509Cert = response.find(
        ns_moa+'SignerInfo').find(
            ns_dsig+'X509Data').find(
                ns_dsig+'X509Certificate').text
    if base64Compare(x509Cert, login_info.get(
        'signer_certificate', 'INVALID')) == False:
        return ([0,0,0,0,1], None)
    hash_items = response.findall(ns_moa+'HashInputData')
    data = []
    for hash_item in hash_items:
        buf_b64 = hash_item.find(ns_moa + 'Base64Content').text
        buf = decodestring(buf_b64)
        if buf.find('SignedProperties') < 0:
            data.append(buf)
    if len(data) != 1:
        return [0], None
    # Ok, we have the data now, now let's parse it and return the XML Root
    sdata = ET.XML(data[0]) 
    return [0], sdata
    
    
def base64Compare(s1, s2):
    """Compare two base64 strings"""
    s1 = s1.replace("\n", "")
    s1 = s1.replace("\r", "")
    s2 = s2.replace("\n", "")
    s2 = s2.replace("\r", "")
    return s1 == s2

class MoaIDAuth(object):

    def __init__(self, moaurl):
        self.moaurl = moaurl

    def parse_response(self, response):
        saml = response.find(
            ns_samla+'Assertion').find(
            ns_samla+'AttributeStatement')
        attribs = saml.findall(ns_samla + 'Attribute')
        person = None
        mandate = None
        mandator = None
        repres = None
        signer_certificate = None
        for attrib in attribs:
            if attrib.attrib['AttributeName'] == 'PersonData':
                person = attrib.find(ns_samla+'AttributeValue').find(
                    ns_person+'Person')
            if attrib.attrib['AttributeName'] == 'Mandate':
                mandate = attrib.find(ns_samla+'AttributeValue').find(
                    ns_mandate+'Mandate')
            if attrib.attrib['AttributeName'] == 'SignerCertificate':
                signer_certificate=attrib.find(ns_samla+'AttributeValue').text
                
        if person is not None:
            person = read_person(person)
        if mandate is not None:
            # Read Representative and Mandator
            xml_person = mandate.find(ns_mandate+'Representative').find(
                ns_person+'PhysicalPerson')
            repres = read_person(xml_person)
            mandator = {}
            xml_mandator = mandate.find(ns_mandate+'Mandator')
            xml_corp = xml_mandator.find(ns_person+'CorporateBody')
            mandator['regno'] = xml_corp.find(
                ns_person+'Identification').find(
                ns_person+'Value').text
            mandator['name'] = xml_corp.find(
                ns_person+'FullName').text

        return {'person' : person, 
                'repres' : repres, 
                'mandator' : mandator, 
                'signer_certificate' : signer_certificate}


    def __call__(self, saml_artifact):
        """Do the authentication"""
        # Create request string from template
        tree = ET.parse(os.path.join(tmpl_dir,
            "tmpl/MOA-ID-AUTH-GetAuthenticationData-REQUEST.xml"))
        root = tree.getroot()
        samlp = root.find(ns_soap+'Body').find(
            ns_samlp+'Request')
        samlp.attrib['IssueInstant'] = soaptime()
        # Request ID that comes back later on
        request_id = str(randrange(
            1000000000000000,
            9999999999999999))
        samlp.attrib['RequestID'] = request_id
        # Set SAML Assertion Artifact
        samlp.find(ns_samlp+'AssertionArtifact').text = saml_artifact
        # Convert to string
        soap_data = ET.tostring(root, 'UTF-8')
        
        # Send request to moa-id
        req = urllib2.Request(url=self.moaurl,
                              data = soap_data)
        req.add_header('Content-type', 'text/xml')
        req.add_header('SOAPAction', '')
        req.add_header('Cache-Control', 'no-cache')
        req.add_header('Pragma', 'no-cache')
        req.add_header('Connection', 'keep-alive')
        f = urllib2.urlopen(req)

        # Read and interprete result
        result = f.read()
        # Save result
        #fd = open("/tmp/bk-result.xml", 'w')
        #fd.write(result)
        #fd.close()
        # Parse result into element tree
        root = ET.XML(result)
        response = root.find(ns_soap+'Body').find(
            ns_samlp+'Response')
        if response.attrib['InResponseTo'] != request_id:
            raise MoaIDAuthException("RequestID / InResponseTo differ!")
        # Check, if response contains errors
        status = response.find(ns_samlp + 'Status')
        status_code = status.find(ns_samlp + 'StatusCode').attrib['Value']
        status_text = status.find(ns_samlp + 'StatusMessage').text
        
        if status_code != "samlp:Success":
            raise MoaIDAuthException("%s: %s" % (status_code, status_text))
        
        # Retrieve information out of resulting XML file and return it
        return self.parse_response(response)
        


if __name__ == '__main__':
    m = MoaIDAuth('http://egov.act.at/moa-id-auth/services/GetAuthenticationData')
    #m('abc')
    retrieveData()

    
