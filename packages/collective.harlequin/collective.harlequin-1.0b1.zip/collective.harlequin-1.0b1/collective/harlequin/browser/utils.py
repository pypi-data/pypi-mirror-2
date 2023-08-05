from Products.Five import BrowserView
from collective.harlequin.interfaces import IHarlequinView
from zope import interface
from zope import component

class IsetTemplateIdHelper(interface.Interface):
    """Allowed interface"""

    def isConfigurableView(templateId):
        """Check if this view is configurable"""

    def getFormName(templateId):
        """return the form name"""

class setTemplateIdHelper(BrowserView):
    """simple helper"""
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.cview = None
        self.templateId = ""

    def isConfigurableView(self, templateId):
        """Check if this view is configurable"""
        #try to find a browser view with getForName
        view = self.context.restrictedTraverse(templateId)
        return IHarlequinView.providedBy(view)

    def getFormName(self, templateId):
        return "%s.form"%templateId
