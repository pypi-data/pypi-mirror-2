import unittest
from Testing import ZopeTestCase as ztc
from collective.harlequin.tests import base

def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'storage.txt', package='collective.harlequin',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='collective.harlequin.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'test_integration.txt', package='collective.harlequin',
        #    test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'test_integration.txt', package='collective.harlequin',
            test_class=base.TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
