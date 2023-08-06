## Controller Python Script "collective_folderposition"
##title=Move objects in a ordered folder
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=collective_folderposition, paths, delta=1
##

from Products.CMFPlone import PloneMessageFactory as _

position=collective_folderposition.lower()

ids = [path.rsplit('/', 1)[1] for path in paths]

if   position=='up':
    context.moveObjectsUp(ids, delta)
elif position=='down':
    context.moveObjectsDown(ids, delta)
elif position=='top':
    context.moveObjectsToTop(ids)
elif position=='bottom':
    context.moveObjectsToBottom(ids)

context.plone_utils.reindexOnReorder(context)

msg=_(u'Item\'s position has changed.')
context.plone_utils.addPortalMessage(msg)

return state
