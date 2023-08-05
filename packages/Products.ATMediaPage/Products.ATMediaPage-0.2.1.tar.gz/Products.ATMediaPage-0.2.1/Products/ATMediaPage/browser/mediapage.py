from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.ATMediaPage import ATMediaPageMessageFactory as _


class MediaPageView(BrowserView):
    """MediaPage browser view."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_images(self):
        """Get all images inside the mediapage."""
        images = []
        path = '/'.join(self.context.getPhysicalPath())
        query = {}
        query['path'] = {'query': path, 'depth': -1}
        query['portal_type'] = ('Image', )
        query['sort_on'] = 'getObjPositionInParent'
        
        for image in self.portal_catalog.searchResults(query):
            images.append({
                'id': image.id,
                'title': image.Title,
                'description': image.Description,
                'url': image.getURL(),
            })
        
        return images
