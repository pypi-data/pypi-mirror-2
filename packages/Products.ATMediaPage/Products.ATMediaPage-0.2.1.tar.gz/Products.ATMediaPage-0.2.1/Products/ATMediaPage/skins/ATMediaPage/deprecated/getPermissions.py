## Script (Python) "getPortalProps_py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

#AUTHENTICATED_USER.has_permission('View', this())

if context.portal_membership.checkPermission('Modify portal content', context):
    return True
