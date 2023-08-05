import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite(extension_profiles=("collective.harlequin:default",))

import collective.harlequin


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(collective.harlequin)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

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
            test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'storage.txt', package='collective.harlequin',
            test_class=TestCase),


        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
