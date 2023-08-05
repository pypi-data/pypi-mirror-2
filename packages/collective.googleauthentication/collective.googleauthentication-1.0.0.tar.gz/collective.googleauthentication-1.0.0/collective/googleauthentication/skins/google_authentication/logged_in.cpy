## Controller Python Script "logged_in"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Initial post-login actions
##

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

REQUEST=context.REQUEST

membership_tool=getToolByName(context, 'portal_membership')

if REQUEST.get('token'):

	google_token = REQUEST.get('token')
	
	session_token = context.restrictedTraverse("session_token")
	google_token = session_token.convert_to_a_session_token(google_token)
	
	member = membership_tool.getAuthenticatedMember()
	member.setProperties(google_token=google_token)
	
else:
	if membership_tool.isAnonymousUser():
		REQUEST.RESPONSE.expireCookie('__ac', path='/')
		context.plone_utils.addPortalMessage(_(u'Login failed. Both login name and password are case sensitive, check that caps lock is not enabled.'), 'error')
		return state.set(status='failure')

	membership_tool.loginUser(REQUEST)


member = membership_tool.getAuthenticatedMember()
if member.getProperty('google_token')=='':

	came_from = REQUEST.get('came_from', None)

	session_token = context.restrictedTraverse("session_token")
	url = session_token.get_auth_sub_url(came_from)
	
	REQUEST.RESPONSE.redirect(url)
	return

login_time = member.getProperty('login_time', '2000/01/01')
initial_login = int(str(login_time) == '2000/01/01')
state.set(initial_login=initial_login)

must_change_password = member.getProperty('must_change_password', 0)
state.set(must_change_password=must_change_password)

if initial_login:
	state.set(status='initial_login')
elif must_change_password:
	state.set(status='change_password')

return state
