## Script (Python) "selectViewTemplate"
##title=Helper method to select a view template
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=templateId

util = context.restrictedTraverse('@@selectViewTemplate.utils')

if util.isConfigurableView(templateId):
    target_url = context.absolute_url() + '/' + util.getFormName(templateId) + '?form.widgets.templateId=' + templateId
    return context.REQUEST.RESPONSE.redirect(target_url)
else:
    #old code
    from Products.CMFPlone import PloneMessageFactory as _
    context.setLayout(templateId)
    context.plone_utils.addPortalMessage(_(u'View changed.'))

return state
