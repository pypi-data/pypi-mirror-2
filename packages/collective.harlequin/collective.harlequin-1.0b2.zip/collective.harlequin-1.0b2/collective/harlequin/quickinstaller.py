from Products.CMFQuickInstallerTool.interfaces import INonInstallable
from zope.interface import implements

class HiddenProfiles(object):
    """Hide some eggs from QuickInstaller"""
    implements(INonInstallable)

    def getNonInstallableProducts(self):

        return ["collective.harlequin"]
