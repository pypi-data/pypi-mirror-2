## Script (Python) "selectViewTemplate"
##title=Helper method to select a view template
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=templateId

view = context.restrictedTraverse(templateId)
if hasattr(view, 'toggle_display_form'):
    view.toggle_display_form()

#original code taken from Plone3.3
from Products.CMFPlone import PloneMessageFactory as _
context.setLayout(templateId)
context.plone_utils.addPortalMessage(_(u'View changed.'))

return state
