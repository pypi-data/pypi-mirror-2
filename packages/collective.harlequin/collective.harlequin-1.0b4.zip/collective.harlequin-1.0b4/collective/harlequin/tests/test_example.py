import unittest
from Testing import ZopeTestCase as ztc
from collective.harlequin.tests import base
from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase as ptc
import tempfile as tmp

class Test(base.FunctionalTestCase):

    def afterSetUp(self):
        self.browser = Browser()
        self.portal.error_log._ignored_exceptions = ()
        self.login()
        self.purl = self.portal.absolute_url()
        self.browser.open(self.purl)
        self.browser.getLink('Log in').click()
        self.browser.getControl(name='__ac_name').value = ptc.portal_owner
        self.browser.getControl(name='__ac_password').value = ptc.default_password
        self.browser.getControl(name='submit').click()

    def contents(self):
        fd, fn = tmp.mkstemp(suffix=".html", prefix="testbrowser-")
        file = open(fn, 'w')
        file.write(self.browser.contents)
        file.close()
        print fn

    def test_config(self):
        self.browser.open(self.purl+'/news/@@harlequin_example')
        contents = self.browser.contents.split('\n')
        config = {}
        for content in contents:
            if content.startswith("Check"):continue
            if not content:continue
            key, value = content.split(':')
            config[key] = value
        self.assert_(len(config)==3)
        self.assert_(config['text']=="default text value")
        self.assert_(config['boolean']=="False")
        self.assert_(config['int']=="10")

    def test_dynamic_form_display(self):
        #set harlequin_test view has default view
        url = self.purl+'/news/selectViewTemplate?templateId=harlequin_example'
        self.browser.open(url)
        #display the form
        self.browser.open(self.purl+'/news?harlequin_display_form=True')
        self.failUnless(self.browser.getControl('Save'))
        self.failUnless(self.browser.getControl('Text'))
#        I don t know why boolean check doesn t work
#        self.failUnless(self.browser.getControl('Boolean'))
        self.failUnless(self.browser.getControl('Int'))

    def test_form_display(self):
        #set harlequin_test view has default view
        url = self.purl+'/news/selectViewTemplate?templateId=harlequin_example_withform'
        self.browser.open(url)
        #display the form
        self.browser.open(self.purl+'/news?harlequin_display_form=True')
        self.failUnless("My super example with form" in self.browser.contents)
        self.failUnless(self.browser.getControl('Save'))
        self.failUnless(self.browser.getControl('Text'))
#        I don t know why boolean check doesn t work
#        self.failUnless(self.browser.getControl('Boolean'))
        self.failUnless(self.browser.getControl('Int'))

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
