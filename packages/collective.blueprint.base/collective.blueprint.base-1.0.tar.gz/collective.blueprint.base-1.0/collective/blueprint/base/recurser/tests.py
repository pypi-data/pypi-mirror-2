import unittest
from zope.testing import doctest

from Products.Five import zcml

from collective.transmogrifier.sections import tests

from collective.blueprint.base.configsource import (
    tests as configsource_tests)
from collective.blueprint.base import recurser

def setUp(test):
    configsource_tests.setUp(test)
    zcml.load_config('configure.zcml', recurser)

def test_suite():
    suite = doctest.DocFileSuite(
        'README.txt',
        optionflags=(
            doctest.NORMALIZE_WHITESPACE|
            doctest.ELLIPSIS|
            doctest.REPORT_NDIFF),
        setUp=setUp, tearDown=tests.tearDown)
    return unittest.TestSuite([suite])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
