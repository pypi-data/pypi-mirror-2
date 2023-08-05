from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.criteria.base import ATBaseCriterion

def syncTopicCriteria(canonical, translation):
    portal = getToolByName(canonical, 'portal_url').getPortalObject()
    portal_types = getToolByName(canonical, 'portal_types')

    
    # get the translated object by taking the first part of the url
    copyids = []
    for object in canonical.objectValues():

        if object.getId().startswith('crit_'):
            # copy the criteria over to the new translated smart folder
            
            # save content type restrictions and change them temporarily
            # so we are allowed to add criteria objects to the smart folder
            # by default only smart folders can be added to smart folders
            
            crit_type = getattr(portal_types, object.portal_type)
            topic_type = getattr(portal_types, translation.portal_type)
            global_allow = crit_type.global_allow
            filter = topic_type.filter_content_types
            
            crit_type.global_allow = True
            topic_type.filter_content_types = False
            if hasattr(translation, object.getId()):
                translation.manage_delObjects([object.getId()])
            copy = canonical.manage_copyObjects([object.getId()])
            translation.manage_pasteObjects(copy)
                
            # restore the original restrictions
            crit_type.global_allow = global_allow
            topic_type.filter_content_types = filter
