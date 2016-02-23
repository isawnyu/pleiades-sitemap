Introduction
============

Sort catalog brains by creation timestamp, collect in batches for sitemaps
and index the batches.

To test the class that does the batching, we'll use a list of brain-like objects:

  >>> class MockBrain(object):
  ...     CreationDate = '2009-09-10 08:19:54'
  ...     def __init__(self, **kw):
  ...         for key, value in kw.items():
  ...             setattr(self, key, value)
  ...     def getURL(self):
  ...         return self.url
  ...     def getPath(self):
  ...         return '/plone' + self.url.replace('http://example.com', '')
  
  >>> from datetime import datetime
  >>> source = [MockBrain(Title='%d'%i, url='http://example.com/%d'%i, ModificationDate=datetime.fromtimestamp(1254215834 + 100000*i).isoformat()) for i in range(3)]
  >>> from pleiades.sitemap import SitemapIndex
  >>> index = SitemapIndex(urlbase='http://example.com', batchsize=1, gzip=True)
  >>> index.process(source)
  >>> len(index)
  3
  >>> sitemap0 = index[0]
  >>> len(sitemap0)
  1
  >>> sitemap0.name
  'sitemap-1'
  >>> sitemap0.lastmod
  '2009-09-29T02:17:14Z'
  >>> url00 = sitemap0[0]
  >>> url00.path
  '/0'
  >>> url00.lastmod
  '2009-09-29T02:17:14Z'
  >>> index[1].lastmod == index[1][0].lastmod
  True
  >>> index[2].lastmod == index[2][0].lastmod
  True

Test the writer

  >>> from pleiades.sitemap import SitemapWriter
  >>> import tempfile, os
  >>> tempdir = tempfile.mkdtemp()
  >>> writer = SitemapWriter()
  >>> writer.write(index, tempdir)
  >>> print os.listdir(tempdir)
  ['sitemap-1.xml.gz', 'sitemap-2.xml.gz', 'sitemap-3.xml.gz', 'sitemap.xml']
  
And again

Test the writer

  >>> writer.write(index, '/tmp')
  
  