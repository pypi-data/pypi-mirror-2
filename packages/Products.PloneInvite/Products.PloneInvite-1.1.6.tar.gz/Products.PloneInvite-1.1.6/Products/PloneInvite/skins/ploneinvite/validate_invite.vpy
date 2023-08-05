## Controller Script Python "validate_invite"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state  
##bind subpath=traverse_subpath
##parameters=invite_to_address='',invitecode=None
##title=validates the email adresses

# Import "PloneMessageFactory as _" to create messages in the plone domain
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
reg_tool = getToolByName(context, 'portal_registration')

if not invite_to_address:
    state.setError('invite_to_address', _(u'Email address is a mandatory field.'), 'email_required') 

if invite_to_address and not reg_tool.isValidEmail(invite_to_address):
    state.setError('invite_to_address', _(u'Please submit a valid email address.'), 'email_required') 

if state.getErrors():
    state.set(status='failure', portal_status_message=_(u'Please correct the indicated errors test.')) 

return state
