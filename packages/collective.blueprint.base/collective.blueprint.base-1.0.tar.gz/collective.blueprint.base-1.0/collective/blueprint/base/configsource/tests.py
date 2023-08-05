import unittest
from zope.testing import doctest

from Products.Five import zcml

from collective.transmogrifier.sections import tests

from collective.blueprint.base import configsource

def setUp(test):
    tests.sectionsSetUp(test)
    zcml.load_config('configure.zcml', configsource)

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
