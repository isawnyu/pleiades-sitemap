from optparse import OptionParser

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from pleiades.dump import secure
from pleiades.sitemap import SitemapIndex, SitemapWriter


class PlacesWriter(object):
    
    def __call__(self, context, destination):
        index = SitemapIndex(
                    'http://pleiades.stoa.org', 
                    batchsize=10000, 
                    gzip=True
                    )
        catalog = getToolByName(site, 'portal_catalog')
        results = catalog.searchResults(
                    portal_type='Place',
                    review_state='published',
                    sort_on='created',
                    sort_order='ascending'
                    )
        index.process(results)
        writer = SitemapWriter()
        writer.write(index, destination)
        

if '__name__' == '__main__':

    parser = OptionParser()
    parser.add_option(
        "-d", "--destination", dest="destination",
        help="Sitemap file(s) destination")
    opts, args = parser.parse_args(sys.argv[1:])

    site = app['plone']
    secure(site, 'admin')
    PlacesWriter()(site, opts.destination)

