## Controller Python Script "properties_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=REQUEST,id=''
##title=Edit content properties
##
# if there is no id specified, keep the current one
if not id:
    id = context.getId()
new_context = context.portal_factory.doCreate(context, id)

new_context.manage_editProperties(REQUEST=REQUEST)
context.plone_utils.addPortalMessage('Properties updated.')
return state.set(context=new_context)

