## Controller Python Script "login_next"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Login next actions
##

from Products.CMFPlone import PloneMessageFactory as _

REQUEST = context.REQUEST

util = context.plone_utils
membership_tool=context.portal_membership
if membership_tool.isAnonymousUser():
    REQUEST.RESPONSE.expireCookie('__ac', path='/')
    util.addPortalMessage(_(u'Login failed'), 'error')
    return state.set(status='failure')

came_from = REQUEST.get('came_from', None)

# if we weren't called from something that set 'came_from' or if HTTP_REFERER
# is the 'logged_out' page, return the default 'login_success' form
if came_from is not None:
    scheme, location, path, parameters, query, fragment = util.urlparse(came_from)
    util.addPortalMessage(_(u'Welcome! You are now logged in.'))
    came_from = util.urlunparse((scheme, location, path, parameters, query, fragment))

    # redirect immediately
    return REQUEST.RESPONSE.redirect(came_from)

state.set(came_from=came_from)

return state
