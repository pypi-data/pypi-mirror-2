from collective.harlequin.interfaces import IHarlequinStorage
from collective.harlequin import _

from plone.app.z3cform import layout

from zope import interface
from zope import schema

from z3c.form import button, field, form
from z3c.form.interfaces import HIDDEN_MODE

class Schema(interface.Interface):
    """Base schema for config form"""

    templateId = schema.TextLine(title=_("templateId"), required=True)

class Form(form.Form):

    fields = field.Fields(Schema)

    label = _(u"Harlequin base form")
    ignoreContext = True

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):
        data, errors = self.extractData()
        templateId = data['templateId']
        self.setLayout(templateId)
        self.saveConfiguration(data)
        self.request.response.redirect(self.nextURL())

    def setLayout(self, templateId):
        self.context.setLayout(templateId)

    def saveConfiguration(self, configuration):
        storage = IHarlequinStorage(self.context)
        storage.set(configuration)

    def updateWidgets(self):
        super(Form, self).updateWidgets()
        self.widgets['templateId'].mode = HIDDEN_MODE
        config = IHarlequinStorage(self.context).get()
        for k in config.keys():
            if k in self.widgets.keys() and k != 'templateId':
                self.widgets[k].value = config[k]

    def nextURL(self):
        return self.context.absolute_url() + '/view'

    def cancelURL(self):
        return self.nextURL()

    @button.buttonAndHandler(_(u'Cancel'))
    def handleApply(self, action):
        self.context.response.redirect(self.cancelURL())


class Page(layout.FormWrapper):

    form = Form
