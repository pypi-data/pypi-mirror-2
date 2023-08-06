##bind state=state
##parameters=title

form = context.REQUEST.form
id = form.get('id', None)
context.setTitle(title)
if id:
    context.setId(id)
message = "Node has been saved"
return state.set(portal_status_message=message)
