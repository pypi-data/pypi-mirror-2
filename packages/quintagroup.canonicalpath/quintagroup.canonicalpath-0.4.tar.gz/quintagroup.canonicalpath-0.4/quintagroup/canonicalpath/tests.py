import unittest

from zope.testing import doctestunit
from zope.component import testing
from zope.component import queryAdapter, queryMultiAdapter
from plone.indexer.interfaces import IIndexableObject
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

from Products.Archetypes.tests.utils import makeContent

from quintagroup.canonicalpath.interfaces import ICanonicalPath

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            import quintagroup.canonicalpath
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', quintagroup.canonicalpath)
            fiveconfigure.debug_mode = False

ptc.setupPloneSite()

class TestAdapter(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.my_doc = makeContent(self.portal, portal_type='Document', id='my_doc')
        self.purl = getToolByName(self.portal, 'portal_url')
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.logout()

    def testAdapter4Portal(self):
        cpadapter = queryAdapter(self.portal, ICanonicalPath)
        self.assertFalse(cpadapter is None,
            "Can't get canonical path adapter for the plone site object")


        portal_cp = '/'+'/'.join(self.purl.getRelativeContentPath(self.portal))
        adcp = cpadapter.canonical_path()
        self.assertTrue(adcp == portal_cp, "Canonical path adapter return '%s' "\
            "for portal, must be: '%s'" % (adcp, portal_cp) )


    def testAdapter4AT(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        self.assertFalse(cpadapter is None,
            "Can't get canonical path adapter for the Document object")

        mydoc_cp = '/'+'/'.join(self.purl.getRelativeContentPath(self.my_doc))
        adcp = cpadapter.canonical_path()
        self.assertTrue(adcp == mydoc_cp, "Canonical path adapter return '%s' "\
            "for document, must be: '%s'" % (adcp, mydoc_cp) )


    def testIndexerRegistration(self):
        wrapper = queryMultiAdapter((self.portal, self.catalog), IIndexableObject)
        self.assertFalse(wrapper is None, "No indexer registered for portal object")

        wrapper = queryMultiAdapter((self.my_doc, self.catalog), IIndexableObject)
        self.assertFalse(wrapper is None, "No indexer registered for document object")
        
        
def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestAdapter),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
