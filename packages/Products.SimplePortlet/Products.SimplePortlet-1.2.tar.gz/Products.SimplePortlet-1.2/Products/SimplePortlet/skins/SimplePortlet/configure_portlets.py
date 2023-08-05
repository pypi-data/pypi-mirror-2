## Script (Python) "configure_portlets"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=configure_portlets
##

context.portlet_manager.configurePortlets(context)
qst='?portal_status_message=Portlet configuration changed.'
context.REQUEST.RESPONSE.redirect( context.absolute_url() + '/portlet_setup' + qst )