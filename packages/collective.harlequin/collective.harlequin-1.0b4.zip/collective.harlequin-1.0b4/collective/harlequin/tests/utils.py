from collective.harlequin import browser
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
        self.data = {"harlequin_display_form":True}
    
    def get(self):
        return self.data
    
    def set(self, configuration):
        self.data = configuration
