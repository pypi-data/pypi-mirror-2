from collective.harlequin.interfaces import IHarlequinStorage
from collective.harlequin import _

from plone.app.z3cform import layout

from zope import interface
from zope import schema

from z3c.form import button, field, form
from z3c.form.interfaces import HIDDEN_MODE

class Schema(interface.Interface):
    """Base schema for config form"""

    display_form = schema.Bool(title=_(u"display_form"), default=False)

class Form(form.Form):
    """Form"""

    fields = field.Fields(Schema)

    label = _(u"Harlequin base form")
    ignoreContext = True

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):
        data, errors = self.extractData()
        self.saveConfiguration(data)
        self.request.response.redirect(self.context.absolute_url() + '/view')

    def saveConfiguration(self, configuration):
        storage = IHarlequinStorage(self.context)
        configuration['display_form'] = False
        storage.set(configuration)

    def updateWidgets(self):
        super(Form, self).updateWidgets()
#        self.widgets['display_form'].mode = HIDDEN_MODE
        config = IHarlequinStorage(self.context).get()
        for k in config.keys():
            if k in self.widgets.keys():
                self.widgets[k].value = config[k]



class Page(layout.FormWrapper):
    """Page that display the default form"""

    form = Form
