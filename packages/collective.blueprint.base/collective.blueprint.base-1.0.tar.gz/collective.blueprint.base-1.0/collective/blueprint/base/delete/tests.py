import unittest
from zope.testing import doctest
from Testing import ZopeTestCase

from Products.Five import zcml

from collective.transmogrifier.sections import tests

from collective.blueprint.base.configsource import (
    tests as configsource_tests)
from collective.blueprint.base import delete

def setUp(test):
    configsource_tests.setUp(test)
    zcml.load_config('configure.zcml', delete)

class TestCase(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        self.folder.manage_addFile('foo')

    def beforeTearDown(self):
        if hasattr(self.folder, 'foo'):
            self.folder.manage_deleteObjects(['foo'])

def test_suite():
    suite = ZopeTestCase.ZopeDocFileSuite(
        'README.txt',
        optionflags=(
            doctest.NORMALIZE_WHITESPACE|
            doctest.ELLIPSIS|
            doctest.REPORT_NDIFF),
        setUp=setUp, tearDown=tests.tearDown,
        test_class=TestCase)
    return unittest.TestSuite([suite])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
