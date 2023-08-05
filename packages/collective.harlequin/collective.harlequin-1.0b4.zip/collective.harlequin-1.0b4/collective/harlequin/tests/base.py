import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

from collective.testcaselayer import ptc as tcl_ptc
from collective.testcaselayer import common

class Layer(tcl_ptc.BasePTCLayer):
    """Install collective.foo"""

    def afterSetUp(self):
        ztc.installPackage('collective.harlequin')

        import collective.harlequin
        import collective.harlequin.example
        self.loadZCML('configure.zcml', package=collective.harlequin)
        self.loadZCML('configure.zcml', package=collective.harlequin.example)

        self.addProfile('collective.harlequin:default')

layer = Layer([common.common_layer])


#ptc.setupPloneSite(extension_profiles=("collective.harlequin:default",))

#import collective.harlequin

class TestCase(ptc.PloneTestCase):
    """ Base test case """

    layer = layer

class FunctionalTestCase(ptc.FunctionalTestCase):
    """Base functional Test Case"""
    
    layer = layer
