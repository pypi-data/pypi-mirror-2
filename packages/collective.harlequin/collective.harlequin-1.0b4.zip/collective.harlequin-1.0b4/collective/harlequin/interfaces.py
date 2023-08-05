from zope import interface
from zope import schema
from plone.app.layout.globals.interfaces import IViewView

class IHarlequinView(interface.Interface):
    """It's a common usecase. View must be configurable. You want"""
    
    harlequin_config = schema.Object(schema.interfaces.IDict)
    harlequin_form = schema.Object(IViewView)
    harlequin_schema = schema.Object(interface.interfaces.IInterface)

    def display_form():
        """Return True/False to know if the form has to be displayed"""

class IHarlequinStorage(interface.Interface):
    """Store your configuration"""

    def set(configuration):
        """Create or update configuration stored in instance."""

    def get():
        """-> dict with configuration like if it was extracted from the form
        """
