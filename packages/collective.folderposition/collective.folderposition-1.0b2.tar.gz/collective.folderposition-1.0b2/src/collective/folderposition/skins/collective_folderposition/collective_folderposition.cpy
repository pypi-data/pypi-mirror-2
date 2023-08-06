## Controller Python Script "collective_folderposition"
##title=Move objects in a ordered folder
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=collective_folderposition, paths, delta=1, selected_obj_paths=None
##

from Products.CMFPlone import PloneMessageFactory as _

position=collective_folderposition.lower()

ids = [path.rsplit('/', 1)[1] for path in paths]

if selected_obj_paths is None:
    subset_ids = None
else:
    subset_ids = [path.rsplit('/', 1)[1] for path in selected_obj_paths]

if   position=='up':
    context.moveObjectsUp(ids, delta, subset_ids)
elif position=='down':
    context.moveObjectsDown(ids, delta, subset_ids)
elif position=='top':
    context.moveObjectsToTop(ids, subset_ids)
elif position=='bottom':
    context.moveObjectsToBottom(ids, subset_ids)

context.plone_utils.reindexOnReorder(context)

msg=_(u'Item\'s position has changed.')
context.plone_utils.addPortalMessage(msg)

return state
