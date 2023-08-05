from Products.Five import BrowserView
from collective.harlequin.interfaces import IHarlequinView
from collective.harlequin.interfaces import IHarlequinStorage
from collective.harlequin import forms
from zope import interface

class Harlequin(BrowserView):
    """Base browserview to be configurable view"""
    interface.implements(IHarlequinView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def harlequin_schema(self):
        """See IHarlequinView"""
        return forms.Schema

    def harlequin_config(self):
        """See IHarlequinView"""
        return IHarlequinStorage(self.context).get()
