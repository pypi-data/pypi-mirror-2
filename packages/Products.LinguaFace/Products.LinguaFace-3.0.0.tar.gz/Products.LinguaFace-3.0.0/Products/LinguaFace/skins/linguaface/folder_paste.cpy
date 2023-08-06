## Controller Python Script "folder_paste"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Paste objects into a folder
##

# overload of standard Plone script
# to place copy of traductions in good translated folder
# after moving or cloning objects

from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import getToolByName
from AccessControl import Unauthorized
from ZODB.POSException import ConflictError

msg=_(u'Copy or cut one or more items to paste.')
linguaface_tool = getToolByName(context, 'linguaface_tool')

if context.cb_dataValid:
    try:
        context.manage_pasteObjects(context.REQUEST['__cp'])
        linguaface_tool.fixTranslationsPath(context)
        from Products.CMFPlone.utils import transaction_note
        transaction_note('Pasted content to %s' % (context.absolute_url()))
        context.plone_utils.addPortalMessage(_(u'Item(s) pasted.'))
        return state
    except ConflictError:
        raise
    except ValueError:
        msg=_(u'Disallowed to paste item(s).')
    except (Unauthorized, 'Unauthorized'):
        msg=_(u'Unauthorized to paste item(s).')
    except: # fallback
        msg=_(u'Paste could not find clipboard content.')

context.plone_utils.addPortalMessage(msg, 'error')
return state.set(status='failure')

