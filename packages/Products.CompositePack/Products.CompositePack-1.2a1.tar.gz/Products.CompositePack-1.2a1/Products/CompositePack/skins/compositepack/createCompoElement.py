##parameters=compopage_path, target_path, target_index

portal = context.portal_url.getPortalObject()

destination = portal.restrictedTraverse(target_path)
factory = destination.manage_addProduct['CompositePack'].manage_addElement

compo = portal.restrictedTraverse(compopage_path)
#new_id = context.generateUniqueId()
new_id = compo.cp_container.generateUniqueIdForCSS()
new_id = factory(id=new_id)
destination.moveObjectToPosition(new_id, int(target_index))
new_ob = getattr(destination, new_id)

uid = context.UID()
new_ob.setTarget(uid)

#compo = portal.restrictedTraverse(compopage_path)
pageDesignUrl = compo.absolute_url() + '/design_view'

return context.REQUEST.RESPONSE.redirect(pageDesignUrl)
