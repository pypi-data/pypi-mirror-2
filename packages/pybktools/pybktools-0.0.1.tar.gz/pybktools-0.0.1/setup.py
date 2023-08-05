from setuptools import setup, find_packages

setup(
    name = "pybktools",
    version = '0.0.1',
    description="Providing Python support for the Austrian Buergerkarte.",
    author = "Hermann Himmelbauer",
    author_email = "dusty@qwer.tk",
    license = "LGPL",
    packages = ['pybktools'],
    install_requires = ['elementtree'],
    test_suite = "pybktools.test",
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt'],
    }
)
