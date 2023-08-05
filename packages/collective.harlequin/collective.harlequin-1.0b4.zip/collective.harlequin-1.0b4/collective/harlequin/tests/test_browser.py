import unittest
from collective.harlequin import browser
from collective.harlequin.tests import utils

class Test(unittest.TestCase):
    
    def setUp(self):
        context = utils.FakeContext()
        self.view = browser.Harlequin(context, {})
        self.view._config_storage = utils.FakeHarlequinStorage()

    def test_harlequin_config(self):
        config = self.view.harlequin_config
        self.assert_('harlequin_display_form' in config)
        self.assert_(config['harlequin_display_form'] is True)

    def test_harlequin_schema(self):
        schema = self.view.harlequin_schema
        self.assert_(schema.__identifier__=='collective.harlequin.forms.Schema')
                     
    def test_harlequin_form(self):
        form = self.view.harlequin_form
        form_class = form.form
        self.assert_(form_class.__module__=="Products.Five.metaclass")
        fields = form_class.fields.keys()
        self.assert_(len(fields)==1)
        self.assert_(fields[0]=='harlequin_display_form')

    def test_display_form(self):
        self.view.request['harlequin_display_form'] = True
        self.assert_(self.view.display_form() is True)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
