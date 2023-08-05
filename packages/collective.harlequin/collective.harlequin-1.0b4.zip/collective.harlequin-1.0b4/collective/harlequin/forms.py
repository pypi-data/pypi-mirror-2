from collective.harlequin.interfaces import IHarlequinStorage
from collective.harlequin import _

from plone.app.z3cform import layout

from zope import interface
from zope import schema

from z3c.form import button, field, form
from z3c.form.browser import text
from z3c.form.interfaces import HIDDEN_MODE

class Schema(interface.Interface):
    """Base schema for config form"""

    harlequin_display_form = schema.Bool(title=_(u"Test bool"), default=True)

class Form(form.Form):
    """Form"""

    fields = field.Fields(Schema)

    label = _(u"Harlequin base form")
    ignoreContext = True

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):
        self.context.plone_log('handle harlequin form')
        data, errors = self.extractData()
        self.saveConfiguration(data)
        self.request.response.redirect(self.context.absolute_url() + '/view')

    def saveConfiguration(self, configuration):
        view = self.get_view()
        if 'harlequin_display_form' in configuration:
            configuration.pop('harlequin_display_form') #never saved this
        storage = IHarlequinStorage(view)
        storage.set(configuration)

    def updateWidgets(self):
        super(Form, self).updateWidgets()
        view = self.get_view()
        config = IHarlequinStorage(view).get()
        for k in config.keys():
            if k in self.widgets.keys():
                self.widgets[k].value = config[k]

    def get_view(self):
        context = self.context
        view = self.context.restrictedTraverse(self.context.getLayout())
        return view

class Page(layout.FormWrapper):
    """Page that display the default form"""

    form = Form
