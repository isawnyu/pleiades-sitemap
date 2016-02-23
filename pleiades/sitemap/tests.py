from Products.PloneTestCase import PloneTestCase as ptc
from zope.component import testing
from zope.testing import doctestunit
import unittest

ptc.setupPloneSite()


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        doctestunit.DocFileSuite(
            'README.txt', package='pleiades.sitemap',
            setUp=testing.setUp, tearDown=testing.tearDown,
        ),

    ])
