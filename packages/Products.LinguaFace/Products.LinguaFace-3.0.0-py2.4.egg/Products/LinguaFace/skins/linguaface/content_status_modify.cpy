## Controller Python Script "content_status_modify"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=workflow_action=None, comment='', effective_date=None, expiration_date=None, *args
##title=handles the workflow transitions of objects
##

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import getToolByName, base_hasattr

linguaface_tool = getToolByName(context, 'linguaface_tool')

if base_hasattr(context, 'hasTranslation') and linguaface_tool.getProperty('synchronise_translations_workflow'):
    translatedObjects =  [x[0] for x in context.getTranslations().values()]
else :
    translatedObjects =  [context]

for tObj in translatedObjects:
    linguaface_tool.doWorkflowAction( tObj,
                                      workflow_action,
                                      comment,
                                      effective_date=effective_date,
                                      expiration_date=expiration_date )




context.plone_utils.addPortalMessage(_(u'Item state changed.'))
return state
