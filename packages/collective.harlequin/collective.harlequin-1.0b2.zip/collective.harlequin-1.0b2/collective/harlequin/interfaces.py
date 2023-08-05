from zope import interface

class IHarlequinView(interface.Interface):
    """It's a common usecase. View must be configurable. You want"""
    
    def harlequin_config():
        """Return the configuration as a dict.
        At least the configuration must have a 'display_form' boolean
        
        -> {'display_form':True, ...}
        """

    def harlequin_form():
        """Return a browser page like object ready to be rendered that embed
        the full configuration form.
        """

    def toggle_display_form():
        """Toggle the value of harlequin_config['display_form'] """

    def display_form():
        """Return True/False to know if the form has to be displayed"""

class IHarlequinStorage(interface.Interface):
    """Store your configuration"""

    def set(configuration):
        """Create or update configuration stored in instance."""

    def get():
        """-> dict with configuration like if it was extracted from the form
        """
