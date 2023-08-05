#!/usr/bin/env python24
import unittest
from doctest import DocFileSuite, REPORT_ONLY_FIRST_FAILURE

def test_suite():
    suite = DocFileSuite('README.txt', 'latex.txt', 'wildcard.txt',
                         optionflags = REPORT_ONLY_FIRST_FAILURE)
    return suite

if __name__ == '__main__':
    """ Run all tests """

    unittest.TextTestRunner().run(test_suite())
    unittest.main()
