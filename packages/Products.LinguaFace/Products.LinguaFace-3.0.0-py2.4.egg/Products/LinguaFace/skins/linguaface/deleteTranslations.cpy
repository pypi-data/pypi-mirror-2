##parameters=languages=None
##title=

from Products.CMFPlone.utils import transaction_note
REQUEST = context.REQUEST
titles = []
titles_and_ids = []

if languages is None:
    languages = []

status = 'success_translate'
message = "Please select one or more items to delete."

if context.getLanguage() in languages:
    # We are deleting the current object. Redirect to the
    # canonical translation instead.
    o = context.getCanonical()
    if context.getCanonical().getLanguage() in languages:
        o = context.aq_parent
    if o is None:
        raise Exception, "Canonical translation object not found"
else:
    o = context

delete_canonical = False
if context.getCanonical().getLanguage() in languages:
    delete_canonical = True
    canonical = context.getCanonical()
    canonical_language = context.getCanonical().getLanguage()
    languages.remove(canonical_language)

for language in languages:
    obj = context.getTranslation(language)
    titles.append(obj.title_or_id())
    titles_and_ids.append('%s (%s)' % (obj.title_or_id(), obj.getId()))
    context.removeTranslation(language)

if delete_canonical:
    obj = canonical
    titles.append(obj.title_or_id())
    titles_and_ids.append('%s (%s)' % (obj.title_or_id(), obj.getId()))
    canonical.removeTranslation(canonical_language)

if languages:
    transaction_note('Deleted translation(s) %s' % (', '.join(titles_and_ids),))
    message = '%s has been deleted.' % (', '.join(titles),)

return state.set(context=o, status=status, portal_status_message=message)
