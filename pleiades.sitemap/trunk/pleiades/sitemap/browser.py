from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from pleiades.sitemap import SitemapIndex, SitemapWriter


class PlacesSitemapDumper(BrowserView):
    
    def __call__(self):
        index = SitemapIndex(
                    'http://pleiades.stoa.org', 
                    batchsize=10000, 
                    gzip=True
                    )
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog.searchResults(
                    portal_type='Place',
                    review_state='published',
                    sort_on='created',
                    sort_order='ascending'
                    )
        index.process(results)
        writer = SitemapWriter()
        writer.write(index, '/tmp')
        
        return 'Complete'