## Controller Python Script "validate_invitecode"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=invitecode='', email=''
##title=validates the Invite Code of a User

# Import "PloneMessageFactory as _" to create messages in the plone domain
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
mtool = getToolByName(context,'portal_membership')
member = mtool.getAuthenticatedMember()
reg_tool = getToolByName(context, 'portal_registration')
plone_invite = getToolByName(context, 'plone_invite')

def missing(field):
    state.setError(field, _(u'Input is required but no input given.'), 'input_required') 

def invalid(field):
    state.setError(field, _(u'Invite code does not exist or has already been used.'),
                   'invite_invalid') 
    
if 'Manager' not in member.getRoles(): # Manager can register users without invitation code
    if not invitecode:
        missing('invitecode')

    invites = plone_invite.invites
    invite = invites.get(invitecode, None)

    if invite is None or invite.used:
        invalid('invitecode')

        if invite is not None and invite.enforce_address and invite.sent_address!=email:
            state.setError('email',
                           _(u'Please use the email address with which you have recieved your invitation.'),
                           'invalid_email') 

if state.getErrors():
    return state.set(status='failure', portal_status_message=_(u'Please correct the indicated errors.'))
else:
    return state.set(portal_status_message=_(u'You have been registered.')) #TODO Add support to i18n
