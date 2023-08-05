from setuptools import setup, find_packages

setup(
    name = "sa_tools",
    version = "0.0.1",
    description="SQLAlchemy Tools",
    author = "Hermann Himmelbauer",
    author_email = "dusty@qwer.tk",
    license = "LGPL",
    packages = ['sa_tools', 'sa_tools.tests'],
    test_suite = "sa_tools.test",
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt'],
    }
)

