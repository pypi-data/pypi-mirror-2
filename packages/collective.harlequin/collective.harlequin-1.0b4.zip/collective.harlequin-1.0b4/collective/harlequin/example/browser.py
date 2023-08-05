from collective.harlequin import forms
from collective.harlequin import browser
from collective.harlequin import _
from plone.app.z3cform import layout
from zope import schema
from zope import interface

class Schema(interface.Interface):
    """A test schema"""
    
    text = schema.TextLine(title=_(u"Text"),
                           default=u"default text value")
    boolean = schema.Bool(title=_(u"Boolean"),
                               default=False)
    int = schema.Int(title=_(u"Int"),
                     default=10)

class Browser(browser.Harlequin):
    """A test Browser view"""

    harlequin_schema = Schema


class Form(forms.Form):
    """An other form"""

    label = _(u"My super example with form")
    fields = forms.field.Fields(Schema)

FormPage = layout.wrap_form(Form)

class BrowserWithForm(browser.Harlequin):
    """An other test browser view"""

    harlequin_schema = Schema
    harlequin_form = FormPage
