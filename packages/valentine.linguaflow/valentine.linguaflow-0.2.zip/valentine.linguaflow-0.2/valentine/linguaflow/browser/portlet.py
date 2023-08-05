from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

class InvalidTranslations(BrowserView):
    """ View to find invalid translations and group them for nice display in a
        listing or portlet.

    """
    
    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {'lingua_state' : 'invalid',
                 'sort_on' : 'modified'}
        portal_url = getToolByName(self.context, 'portal_url')
        if portal_url.getPortalObject() == self.context:
            # in the root of plone we show all languages
            query['Language'] = 'all'
        result = catalog(query)
        return result
