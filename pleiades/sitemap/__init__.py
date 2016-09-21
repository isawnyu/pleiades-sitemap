import os
import tempfile

import zope.datetime
from zope.interface import implements, Interface, Attribute


class SitemapIndex(object):
    def __init__(self, urlbase, batchsize=50000, gzip=True):
        self._maps = []
        self.urlbase = urlbase
        self.batchsize = batchsize
        self.gzip = gzip
        
    def process(self, data):
        batchsize = self.batchsize
        nbatches = len(data) / batchsize
        for i in range(nbatches):
            start = batchsize * i
            stop = start + batchsize
            name = 'sitemap-%d' % (i+1)
            sitemap = Sitemap(name)
            sitemap.process(data[start:stop])
            self._maps.append(sitemap)
        if len(data) % batchsize != 0:
            # remainders
            start = nbatches * batchsize
            name = 'sitemap-%d' % (nbatches+1)
            sitemap = Sitemap(name)
            sitemap.process(data[start:])
            self._maps.append(sitemap)
            
    def __len__(self):
        return len(self._maps)
    def __getitem__(self, key):
        return self._maps[key]
    def __iter__(self):
        return iter(self._maps)


class ISitemap(Interface):
    name = Attribute("""Name of sitemap file""")
    lastmod = Attribute("""Last modification of any item in sitemap file""")
    # iter


class Sitemap(object):
    implements(ISitemap)
    
    def __init__(self, name):
        self.name = name
        self._items = []
        self._modtime = 0
    
    def process(self, data):
        for d in data:
            item = SitemapItem(d)
            if item._modtime > self._modtime:
                self._modtime = item._modtime
            self._items.append(item)
        self.lastmod = zope.datetime.iso8601_date(self._modtime)
        
    def __len__(self):
        return len(self._items)
    def __getitem__(self, key):
        return self._items[key]
    def __iter__(self):
        return iter(self._items)


class ISitemapItem(Interface):
    path = Attribute("""Relative URL of sitemapped resource""")
    lastmod = Attribute("""Last modifed timestamp""")


class SitemapItem(object):
    # Adapts a Zope2 catalog brain-like object to the sitemap interface
    implements(ISitemap)
    
    def __init__(self, brain):
        self.path = "/" + brain.getPath().split('/', 2)[2]
        self._modtime = zope.datetime.time(brain.ModificationDate)
        self.lastmod = zope.datetime.iso8601_date(self._modtime)


SITEMAP_HEAD = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
SITEMAP_ITEM = """
   <url>
      <loc>https://pleiades.stoa.org%s</loc>
      <lastmod>%s</lastmod>
   </url>
"""
SITEMAP_FOOT = """</urlset>"""

INDEX_HEAD = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
INDEX_ITEM = """
   <sitemap>
      <loc>%s</loc>
      <lastmod>%s</lastmod>
   </sitemap>
"""
INDEX_FOOT = """</sitemapindex>"""


class SitemapWriter(object):
    def write(self, index, location):
        tempdir = tempfile.mkdtemp()
        sitemap = os.path.join(tempdir, 'sitemap.xml')
        s = open(sitemap, 'w')
        s.write(INDEX_HEAD)
        for sitemap in index:
            filename = os.path.join(tempdir, sitemap.name + '.xml')
            f = open(filename, 'w')
            f.write(SITEMAP_HEAD)
            for item in sitemap:
                f.write(SITEMAP_ITEM % (item.path, item.lastmod))
            f.write(SITEMAP_FOOT)
            f.close()
            loc = "%s/%s.xml" % (index.urlbase, sitemap.name)
            if index.gzip:
                os.system("gzip %s" % filename)
                loc += ".gz"
            s.write(INDEX_ITEM % (loc, sitemap.lastmod))
        s.write(INDEX_FOOT)
        s.close()        
        # Copy to final location
        os.chdir(tempdir)
        os.system("cp sitemap* %s" % location)
        
