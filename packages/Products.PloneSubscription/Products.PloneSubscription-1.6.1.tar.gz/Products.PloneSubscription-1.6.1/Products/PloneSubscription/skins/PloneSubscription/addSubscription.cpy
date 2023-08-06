## Script (Python) "addSubscription"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=ptype='', id='', subscriber_uid=''
##title=Add item to subscriptions
##
# -*- coding: utf-8 -*-
if context.isPrincipiaFolderish:
    pass
else:
    if ptype == "FolderSubscription":
        context=container

from Products.CMFCore.utils import getToolByName
RESPONSE = context.REQUEST.RESPONSE
stool = getToolByName(context, 'portal_subscription')
provider = stool.getProvider()
url = '%s/view' % context.absolute_url()

if provider is None:
    psm = 'psm_subscriptions_provider_cannot_be_accessed'
    return RESPONSE.redirect('%s?portal_status_message=%s' % (url, psm))

ptype = context.REQUEST.form.get('ptype','FolderSubscription')

"""
  LinguaPlone compliance removed because big bug + it's not essential
"""

items = [context]


#raise str([i.getId() for i in items])
for item in items:
    keywords = {}
    if ptype == 'KeywordsSubscription':
        keywords['rpath'] = context.REQUEST.form.get('rpath')
        keywords['keywords'] = item.REQUEST.form.get('keywords')
        keywords['title'] = item.REQUEST.form.get('keywords') # Take keywords as title
    elif ptype == 'ExactSearchSubscription':
        keywords['rpath'] = item.REQUEST.form.get('rpath')
        keywords['indices'] = item.REQUEST.form.get('indices')
        keywords['values'] = item.REQUEST.form.get('values')
        keywords['title'] = item.REQUEST.form.get('keywords') # Take keywords as title
    elif ptype == 'FolderSubscription':
        keywords['rpath'] = item.absolute_url_path()
        if item.meta_type == "Plone Site":
            # In case we are on the root folder, we have to take subscriptions from
            # the portal_subscription tool. Let's hope the Portal site will be
            # an Archetype soon
            keywords['folder'] = stool.UID()
        else:
            keywords['folder'] = item.UID()
        keywords['title'] = item.TitleOrId()
        if item.REQUEST.form.has_key('transitions'):
            keywords['transitions'] = item.REQUEST.form.get('transitions')
        if item.REQUEST.form.has_key('recursive'):
            keywords['recursive'] = item.REQUEST.form.get('recursive')
        if item.REQUEST.form.has_key('workflow'):
            keywords['workflow'] = item.REQUEST.form.get('workflow')
        keywords['transition']="publish"
        if item.REQUEST.form.has_key('title'):
            keywords['fullname'] = item.REQUEST.form.get('title')
        if item.REQUEST.form.has_key('email'):
            keywords['email'] = item.REQUEST.form.get('email')
    elif ptype == 'ContentSubscription':
        keywords['rpath'] = item.absolute_url_path()
        keywords['content'] = item.UID()
        keywords['title'] = item.TitleOrId()
        if item.REQUEST.form.has_key('title'):
            keywords['fullname'] = item.REQUEST.form.get('title')
        if item.REQUEST.form.has_key('email'):
            keywords['email'] = item.REQUEST.form.get('email')
    else:
        raise "Unknown Subscription"

    psm = stool.setSubscription(id=id,
                                ptype=ptype,
                                subscriber_uid=subscriber_uid,
                                **keywords)

return RESPONSE.redirect('%s?portal_status_message=%s' % (url, psm))
