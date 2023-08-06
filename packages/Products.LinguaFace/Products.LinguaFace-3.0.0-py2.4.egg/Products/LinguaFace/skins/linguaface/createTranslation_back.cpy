##parameters=set_language=None, current=None, translate=1
##title=

from DateTime import DateTime
from Products.CMFPlone.utils import transaction_note
REQUEST = context.REQUEST

if set_language is None:
    raise Exception, 'Language not specified'

# Set the language of neutral contents
# If the set_language is the same as the current language we set the neutral
# content to another language
if not context.Language():
    if set_language != current:
        context.setLanguage(current)
    else:
        allLanguages = [lang[0] for lang in context.portal_languages.listSupportedLanguages()]
        otherLanguages = [lang for lang in allLanguages if lang != set_language]
        otherLanguage = otherLanguages[0]
        context.setLanguage(otherLanguage)


# There is no portal factory support atm
context.addTranslation(set_language)
o = context.getTranslation(set_language)

if o is None:
    raise Exception, "New translation object not found"

otype = o.getTypeInfo().getId()
message = context.translate(msgid='message_type_has_been_created',
                            default='${type} has been created.',
                            mapping={'type': otype},
                            domain='linguaplone')
transaction_note('Created %s' % otype)

if o.getTypeInfo().getActionById('edit', None) is None:
    state.setStatus('success_no_edit')

if translate and o.getTypeInfo().getActionById('translate', None):
    state.setStatus('success_translate')

return state.set(context=o, portal_status_message=message)
