import unittest
from zope.testing import doctest

from collective.transmogrifier.sections import tests

def test_suite():
    suite = doctest.DocFileSuite(
        'README.txt',
        optionflags=(
            doctest.NORMALIZE_WHITESPACE|
            doctest.ELLIPSIS|
            doctest.REPORT_NDIFF),
        setUp=tests.sectionsSetUp, tearDown=tests.tearDown)
    return unittest.TestSuite([suite])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
