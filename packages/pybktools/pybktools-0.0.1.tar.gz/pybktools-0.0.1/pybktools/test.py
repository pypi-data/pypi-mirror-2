#!/usr/bin/env python24
import unittest
from doctest import DocFileSuite, REPORT_ONLY_FIRST_FAILURE



def additional_tests():
    suite = DocFileSuite('pybktools.txt',
                         package='pybktools',
                         optionflags = REPORT_ONLY_FIRST_FAILURE)
    return suite

def test_suite():
    return additional_tests()

if __name__ == '__main__':
    """ Run all tests """

    unittest.TextTestRunner().run(test_suite())
    unittest.main()
