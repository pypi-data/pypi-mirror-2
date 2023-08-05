from Products.Five import BrowserView
from collective.harlequin.interfaces import IHarlequinView
from collective.harlequin.interfaces import IHarlequinStorage
from collective.harlequin import forms
from zope import interface

class Harlequin(BrowserView):
    """Base browserview to be configurable view"""
    interface.implements(IHarlequinView)

    def __init__(self, context, request):
        """See interface"""
        self.context = context
        self.request = request
        self.__config_storage = None

    def __call__(self):
        """See interface"""
        if self.display_form():
            #do not render the view, render the form
            form = self.harlequin_form()(self.context.aq_inner, self.request)
            return form.__of__(self.context.aq_inner)()
        return super(Harlequin, self).__call__(self)

    def harlequin_config(self):
        """See IHarlequinView"""
        if not self.__config_storage:
            self.__config_storage = IHarlequinStorage(self.context)
        return self.__config_storage.get()

    def harlequin_form(self):
        """See interface. This method must be override to return the 
        form page object of your configuration."""
        return forms.Page
    
    def toggle_display_form(self):
        """See interface"""
        config = self.harlequin_config()
        config['display_form'] = not config['display_form']
        self.__config_storage.set(config)

    def display_form(self):
        """See interface"""
        config = self.harlequin_config()
        return config['display_form']
