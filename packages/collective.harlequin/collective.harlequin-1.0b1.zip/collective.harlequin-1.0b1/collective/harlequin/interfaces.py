from zope import interface

class IHarlequinView(interface.Interface):
    """It's a common usecase. View must be configurable. You want"""
    
    def harlequin_schema():
        """harlequin need to store the a configuration. To define the 
        configuration you define a zope.schema. This return the schema."""

    def harlequin_config():
        """Return the configuration as a dict. At least the configuration must
        have the templateId
        
        -> {'templateId':'myharlequinview', ...}
        """

class IHarlequinStorage(interface.Interface):
    """Store your configuration"""

    def set(configuration):
        """Create or update configuration stored in instance."""

    def get():
        """-> dict with configuration like if it was extracted from the form
        """
