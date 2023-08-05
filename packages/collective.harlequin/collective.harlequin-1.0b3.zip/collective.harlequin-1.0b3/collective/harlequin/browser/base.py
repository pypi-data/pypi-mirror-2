import copy
from Products.Five import BrowserView
from Products.Five import metaclass
from collective.harlequin.interfaces import IHarlequinView
from collective.harlequin.interfaces import IHarlequinStorage
from collective.harlequin import forms
from plone.app.z3cform import layout
from zope import interface
from zope import schema

class Harlequin(BrowserView):
    """Base browserview to be configurable view"""
    interface.implements(IHarlequinView)

    def __init__(self, context, request):
        """See interface"""
        self.context = context
        self.request = request
        self._config_storage = None
        self._harlequin_form = None
        self._harlequin_config = None

    def __call__(self):
        """See interface"""
        if self.display_form():
            #do not render the view, render the form
            form = self.harlequin_form(self.context.aq_inner, self.request)
            return form.__of__(self.context.aq_inner)()
        return super(Harlequin, self).__call__(self)

    def get_harlequin_config(self):
        """Accessor to harlequin_config."""

        if not self._config_storage:
            self._config_storage = IHarlequinStorage(self)
        if not self._harlequin_config:
            self._harlequin_config = self._config_storage.get()
        
        return self._harlequin_config


    def set_harlequin_config(self, configuration):
        """Mutator to harlequin_config."""
        if not self._config_storage:
            self._config_storage = IHarlequinStorage(self)
        return self._config_storage.set(configuration)

    def get_harlequin_form(self):
        """Accessor to harlequin_form."""
        if not self._harlequin_form:
            self._harlequin_form = self._create_form_page()
        return self._harlequin_form

    def _create_form_page(self):
        """Create a form page based on the schema"""
        form = metaclass.makeClass('HarlequinMetaForm',(forms.Form,), {})
        form.fields = forms.field.Fields(self.harlequin_schema)
        return layout.wrap_form(form)

    def set_harlequin_form(self, formpage):
       """Mutator to harlequin_form."""
       self._harlequin_form = formpage

    def display_form(self):
        """See interface"""
        fields = schema.getFields(self.harlequin_schema)
        test_have_in_request = False
        for field_name in fields:
            if 'form.widgets.'+field_name in self.request.keys():
                test_have_in_request = True
        from_request = bool(self.request.get('harlequin_display_form',False))
        return test_have_in_request or from_request

    harlequin_schema = forms.Schema
    harlequin_form   = property(get_harlequin_form,   set_harlequin_form)
    harlequin_config = property(get_harlequin_config, set_harlequin_config)

