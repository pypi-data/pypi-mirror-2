import unittest
from collective.harlequin.browser import base as browser
from collective.harlequin.tests import utils

class Test(unittest.TestCase):
    
    def setUp(self):
        context = utils.FakeContext()
        self.view = browser.Harlequin(context, {})
        self.view._config_storage = utils.FakeHarlequinStorage()

    def test_harlequin_config(self):
        config = self.view.harlequin_config
        self.assert_('test' in config)
        self.assert_(config['test'] is True)

    def test_harlequin_schema(self):
        pass

    def test_harlequin_form(self):
        pass

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
