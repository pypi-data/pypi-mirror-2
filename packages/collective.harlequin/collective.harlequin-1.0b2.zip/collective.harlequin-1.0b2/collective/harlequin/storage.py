"""Store you configuration by using propertymanager or annotation"""
from zope import component
from zope import interface
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from collective.harlequin.interfaces import IHarlequinStorage
from OFS.interfaces import IPropertyManager
from persistent.dict import PersistentDict

class PropertyStorage(object):
    """Implements IHarlequinStorage with OFS.PropertyManager"""

    interface.implements(IHarlequinStorage)
    component.adapts(IPropertyManager)

    def __init__(self, context):
        self.context = context

    def set(self, configuration):
        """see IHarlequinStorage"""

        #TODO: bind configuration types on property types (only str supported atm)

        prefix = self.context.getLayout()

        for id in configuration:

            _id = prefix + '_' + id

            if self.context.hasProperty(_id):
                self.context._delProperty(_id)

            _type = 'string'
            _value = str(configuration[id])

            self.context._setProperty(_id, _value, _type)

    def get(self):
        """see IHarlequinStorage"""

        # TODO: manage default value from schema.

        templateId = self.context.getLayout()
        view = self.context.restrictedTraverse(templateId)
        fields = schema.getFields(view.harlequin_schema())
        config = {}

        for field in fields:
        
            _id = templateId + '_' + field
            config[field] = self.context.getProperty(_id)

        return config

HARLEQUIN_KEY = "collective.harlequin.configuration"

class AnnotationStorage(object):
    """Implements IHarlequinStorage with Annotation"""

    interface.implements(IHarlequinStorage)
    component.adapts(IAttributeAnnotatable)

    def __init__(self, context):

        self.context = context
        self.storage = IAnnotations(context)

    def set(self, configuration):
        """see IHarlequinStorage"""

        if HARLEQUIN_KEY not in self.storage.keys():
            self.storage[HARLEQUIN_KEY] = PersistentDict()

        for key in configuration:
            self.storage[HARLEQUIN_KEY][key] = configuration[key]

    def get(self):
        """see IHarlequinStorage"""

        configuration = {'display_form':False}

        if HARLEQUIN_KEY not in self.storage.keys():
            return configuration

        #is there a faster way to cas persistent dict to dict ?
        for k in self.storage[HARLEQUIN_KEY].keys():
            configuration[k] = self.storage[HARLEQUIN_KEY][k]

        return configuration
