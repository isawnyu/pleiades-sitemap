import sys
from optparse import OptionParser

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from pleiades.dump import secure
from pleiades.sitemap import SitemapIndex, SitemapWriter


class PlacesWriter(object):
    
    def __call__(self, context, destination, gzip=False):
        index = SitemapIndex(
                    'http://pleiades.stoa.org', 
                    batchsize=10000, 
                    gzip=gzip
                    )
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog.searchResults(
                    portal_type='Place',
                    review_state='published',
                    sort_on='created',
                    sort_order='ascending'
                    )
        print len(results)
        index.process(results)
        writer = SitemapWriter()
        writer.write(index, destination)
        

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option(
        "-d", "--destination", dest="destination",
        help="Sitemap file(s) destination")
    parser.add_option(
        "-z", "--zip", dest="gzip", action="store_true", default=False,
        help="GZIP output")
    
    arg_start = [i for (i, v) in enumerate(sys.argv) if '.py' in v][0]
    opts, args = parser.parse_args(sys.argv[arg_start:])

    site = app['plone']
    secure(site, 'admin')
    PlacesWriter()(site, opts.destination, opts.gzip)
