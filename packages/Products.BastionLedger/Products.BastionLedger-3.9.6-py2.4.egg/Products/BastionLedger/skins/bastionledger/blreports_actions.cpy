## Controller Python Script "blreports_actions"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=manage reports folder content
##
request = context.REQUEST
reports = context.Reports
ids = request.get('ids', [])

if request.has_key('form.button.Delete') and ids:
    reports.manage_delObjects(ids)
elif request.has_key('form.button.Paste'):
    reports.manage_pasteObjects(REQUEST=request)
elif request.has_key('form.button.Copy') and ids:
    cp = reports.manage_copyObjects(ids)
    request.RESPONSE.setCookie('__cp', cp, path='%s' % request.get('BASEPATH1', '/'))

return state

