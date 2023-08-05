"""Store you configuration"""
from zope import component
from zope import interface
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from collective.harlequin import interfaces
from persistent.dict import PersistentDict

from Products.CMFCore.utils import getToolByName

HARLEQUIN_KEY = "collective.harlequin.configuration"

class AnnotationStorage(object):
    """Implements IHarlequinStorage with Annotation"""

    interface.implements(interfaces.IHarlequinStorage)
    component.adapts(interfaces.IHarlequinView)

    def __init__(self, view):
        context = view.context.aq_inner
        self.context = context
        self.view = view
        self.schema = view.harlequin_schema
        self.storage = self._annotations()

    def set(self, configuration):
        """see IHarlequinStorage. This implementation take care to save only
        non default values. If other values are found they will be deleted"""

        defaults = self._get_defaults()

        #faster than parsing and cleanup:
        if HARLEQUIN_KEY in self.storage:
            #be sure ZODB remove this
            del self.storage[HARLEQUIN_KEY]

        self.storage[HARLEQUIN_KEY] = PersistentDict()

        for key in configuration:
            if key not in defaults:
                continue
            if configuration[key] == defaults[key]:
                continue
            self.storage[HARLEQUIN_KEY][key] = configuration[key]

    def get(self):
        """see IHarlequinStorage. This implementation return all default 
        values of the schema is nothing has already been saved"""

        defaults = self._get_defaults()

        if HARLEQUIN_KEY not in self.storage.keys():
            return defaults

        configuration = defaults
        #is there a faster way to cast persistent dict to dict ?
        for k in configuration.keys():
            if k in self.storage[HARLEQUIN_KEY]:
                configuration[k] = self.storage[HARLEQUIN_KEY][k]

        return configuration

    def _get_defaults(self):
        """Fields are taken from the schema. 
        
        Return a dict with field name as key and field default
        value as value
        """
        
        defaults = self._get_defaults_schema()
        defaults_properties = self._get_defaults_properties()

        #update defaults with portal data:
        for field_name in defaults:
            if field_name in defaults_properties:
                defaults[field_name] = defaults_properties[field_name]

        return defaults

    def _get_defaults_schema(self):
        """Fields are taken from the schema. 
        
        Return a dict with field name as key and field default
        value as value
        """
        fields = schema.getFields(self.schema)
        defaults = {}
        for field_name in fields:
            defaults[field_name] = fields[field_name].default
        return defaults

    def _get_defaults_properties(self):
        pp = getToolByName(self.context, 'portal_properties')
        if not hasattr(pp, 'harlequin_properties'):
            return {}
        pp = pp.harlequin_properties

        fields = schema.getFields(self.schema)
        defaults = {}
        prefix = self.schema.__identifier__
        for field_name in fields:
            pp_id = prefix+'-'+field_name
            if pp.hasProperty(pp_id):
                defaults[field_name] = pp.getProperty(pp_id)
        return defaults

    def _annotations(self):
        """Return the persistent dict that will embed the configuration"""
        return IAnnotations(self.context)

