import unittest
from Testing import ZopeTestCase as ztc
from collective.harlequin.tests import base, utils
from Products.Five.testbrowser import Browser

class Test(base.FunctionalTestCase):

    def afterSetUp(self):
        self.browser = Browser()
        self.portal.error_log._ignored_exceptions = ()
        self.login()
        self.purl = self.portal.absolute_url()
        self.browser.open(self.purl)
    
    def test_config(self):
        self.browser.open(self.purl+'/news/@@harlequin_test')
        contents = self.browser.contents.split('\n')
        config = {}
        for content in contents:
            if content.startswith("Check"):continue
            if not content:continue
            key, value = content.split(':')
            config[key] = value
        self.assert_(len(config)==3)
        self.assert_(config['text']=="default text value")
        self.assert_(config['bool']=="False")
        self.assert_(config['int']=="10")

    def test_form_display(self):
        form_urls = (self.purl+'/news/selectViewTemplate?templateId=harlequin_test',
                 self.purl+'/news/selectViewTemplate?templateId=harlequin_test_withform')

        for url in form_urls:
            
            self.browser.open(url)
            self.browser.open(self.purl+'/news?harlequin_display_form=True')
            self.failUnless(self.browser.getControl('Save'))
            self.failUnless(self.browser.getControl('text'))
            self.failUnless(self.browser.getControl('bool'))
            self.failUnless(self.browser.getControl('int'))

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
