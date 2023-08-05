import unittest
from collective.harlequin import storage
from collective.harlequin.tests import utils
from zope import schema

class Test(unittest.TestCase):
    
    def setUp(self):
        self.view = utils.MockHarlequinView(utils.fake_context, {})
        #monkey patch to remove dependency on zope.annotation
        def _annotations(self): return {}
        storage.AnnotationStorage._annotations = _annotations
        self.storage = storage.AnnotationStorage(self.view)

    def test_get(self):
        configuration = self.storage.get()
        self.assertEqual(configuration['text'], "default text value")
        self.assertEqual(configuration['bool'], False)
        self.assertEqual(configuration['int'], 10)

    def test_set_not_exists_in_schema(self):
        #first check that non declare information is not stored
        data = {'size':u'400x200'}
        self.storage.set(data)
        configuration = self.storage.get()
        self.failUnless('size' not in configuration.keys())
    
    def test_set_default_not_stored(self):
        #now check that information is well stored
        data = {'text':'An other text',
                'int':15}
        self.storage.set(data)
        stored = self.storage.storage[storage.HARLEQUIN_KEY]
        self.assertEquals(stored['text'], 'An other text')
        self.assertEquals(stored['int'], 15)
        #check default values are not stored
        self.assert_('bool' not in stored.keys())

    def test_set_update_schema_cleanup(self):
        #first do normal things
        self.test_set_default_not_stored()
        data = {'text':'An other text',
                'int':15}
        #let now change the schema and make some more assertions
        self.storage.schema = utils.AnOtherSchema

        #check 'int' has been removed and bool value is True
        self.storage.set(data)
        stored = self.storage.storage[storage.HARLEQUIN_KEY]
        self.assertEquals(stored['text'], 'An other text')
        self.assert_('int' not in stored.keys())

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
