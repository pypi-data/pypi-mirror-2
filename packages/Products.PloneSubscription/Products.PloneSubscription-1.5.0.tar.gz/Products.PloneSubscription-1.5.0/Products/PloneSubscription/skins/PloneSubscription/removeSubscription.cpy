## Controller Python Script "removeSubscription"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id=None
##title=Remove subscription
##
# -*- coding: utf-8 -*-

message = ""
from Products.CMFCore.utils import getToolByName
stool = getToolByName(context, 'portal_subscription')
mtool = getToolByName(context, 'portal_membership')
"""

adaptations to make PloneSubscription LinguaPlone avare
only FolderSubscription and ContentSubscription ist tested so far
adaptations:
  - when PloneLanguage is installed we try to get all translations of an object
  - for each of the translations we test if it is allredy subscribed. if not we subscribe to it

"""
items = [context]
try:
    lang = context.getTranslation()
    objects = context.getTranslations() #returns a dic {language:item, ..}
    for l, item in objects.items():
        if l != lang:
            items.append(item[0])
except:
    pass

for item in items:
    if mtool.isAnonymousUser():
        if id:
            # id is given, so this link comes from an email
            message = stool.removeSubscription(item, subscriber_id = id)
        else:
            email = item.REQUEST.get('email')
            if stool.getAnonymous_unsubscribe_by_email():
                message = stool.unsubscriptionMailing(item, email)
            else:
                message = stool.removeSubscription(item)
    else:
        message = stool.removeSubscription(item)

return state.set(status='success', portal_status_message=message)
