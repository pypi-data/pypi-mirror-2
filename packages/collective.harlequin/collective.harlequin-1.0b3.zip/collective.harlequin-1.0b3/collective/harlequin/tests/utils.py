from collective.harlequin import forms
from collective.harlequin import browser
from collective.harlequin import _
from zope import schema
from zope import interface

class TestSchema(interface.Interface):
    """A test schema"""
    
    text = schema.TextLine(default=u"default text value")
    bool = schema.Bool(default=False)
    int = schema.Int(default=10)

class AnOtherSchema(interface.Interface):
    """An other schema"""

    text = schema.TextLine(default=u"default !")
    bool = schema.Bool(default=True)


class MockHarlequinView(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.harlequin_schema = TestSchema
        self.harlequin_form = None
        self.harlequin_config = {}


class FakeContext(object):
    def __init__(self):
        self.aq_inner = self

fake_context = FakeContext()

class FakeHarlequinStorage(object):
    def __init__(self):
        self.data = {"test":True}
    
    def get(self):
        return self.data
    
    def set(self, configuration):
        self.data = configuration

class MyBrowser(browser.Harlequin):
    """A test Browser view"""

    harlequin_schema = TestSchema

class AnOtherForm(forms.Form):
    """An other form"""
    fields = forms.field.Fields(TestSchema)

class MyBrowserWithForm(browser.Harlequin):
    """An other test browser view"""
    label = _(u"My super test form")
    harlequin_schema = TestSchema
    harlequin_form = AnOtherForm
