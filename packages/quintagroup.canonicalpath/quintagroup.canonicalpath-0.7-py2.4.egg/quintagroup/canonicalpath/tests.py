import unittest

from zope.testing import doctestunit
from zope.component import testing
from zope.component import queryAdapter, queryMultiAdapter, getMultiAdapter
from zope.schema.interfaces import InvalidValue

#for compatibility with older plone versions 
try:
    from plone.indexer.interfaces import IIndexableObject
    IS_NEW = True
except:
    from plone.app.content.interfaces import IIndexableObjectWrapper \
        as _old_IIndexableObjectWrapper
    IS_NEW = False


from OFS.PropertyManager import PropertyManager
from OFS.Traversable import Traversable

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

from Products.Archetypes.tests.utils import makeContent

from quintagroup.canonicalpath.interfaces import ICanonicalPath
from quintagroup.canonicalpath.interfaces import ICanonicalLink
from quintagroup.canonicalpath.adapters import PROPERTY_PATH
from quintagroup.canonicalpath.adapters import PROPERTY_LINK
from quintagroup.canonicalpath.upgrades import CanonicalConvertor

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            import quintagroup.canonicalpath
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', quintagroup.canonicalpath)
            fiveconfigure.debug_mode = False

ptc.setupPloneSite()

class TestIndexerRegistration(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.my_doc = makeContent(self.portal, portal_type='Document', id='my_doc')
        self.logout()

    def get_indexable_wrapper(self, obj):
        if IS_NEW:
            wrapper = None
            if not IIndexableObject.providedBy(obj):
                wrapper = queryMultiAdapter((obj, self.catalog), IIndexableObject)
        else:
            wf = getattr(self.portal, 'portal_workflow', None)
            if wf is not None:
                vars = wf.getCatalogVariablesFor(obj)
            else:
                vars = {}
            wrapper = getMultiAdapter((obj, self.portal), _old_IIndexableObjectWrapper)
            wrapper.update(vars)
            
        return wrapper and wrapper or obj

    def testForAT(self):
        wrapper = self.get_indexable_wrapper(self.my_doc)
        self.assertFalse(wrapper is None, "No indexer registered for document object")

    def testCanonicalPathForAT(self):
        wrapper = self.get_indexable_wrapper(self.my_doc)
        self.assertTrue(hasattr(wrapper, 'canonical_path'),
            "'canonical_path' attribute not accessible with indexer wrapper for Document object")

    def testCanonicalLinkForAT(self):
        wrapper = self.get_indexable_wrapper(self.my_doc)
        self.assertTrue(hasattr(wrapper, 'canonical_link'),
            "'canonical_link' attribute not accessible with indexer wrapper for Document object")


        
class TestDefaultCanonicalPathAdapter(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.purl = getToolByName(self.portal, 'portal_url')
        self.my_doc = makeContent(self.portal, portal_type='Document', id='my_doc')
        self.logout()

        self.mydoc_cp = '/'+'/'.join(self.purl.getRelativeContentPath(self.my_doc))
        self.portal_cp = '/'+'/'.join(self.purl.getRelativeContentPath(self.portal))

    def testRegistration4Portal(self):
        cpadapter = queryAdapter(self.portal, ICanonicalPath)
        self.assertFalse(cpadapter is None,
            "Can't get canonical path adapter for the plone site object")

    def testRegistration4AT(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        self.assertFalse(cpadapter is None,
            "Can't get canonical path adapter for the Document object")
        

    def testGetDefault4Portal(self):
        cpadapter = queryAdapter(self.portal, ICanonicalPath)
        self.assertTrue(cpadapter.canonical_path == self.portal_cp,
            "Canonical path adapter return '%s' for portal, must be: '%s'" % (
            cpadapter.canonical_path, self.portal_cp) )


    def testGetDefault4AT(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        self.assertTrue(cpadapter.canonical_path == self.mydoc_cp,
            "Canonical path adapter return '%s' for document, must be: '%s'" % (
            cpadapter.canonical_path, self.mydoc_cp) )


    def testSet4Portal(self):
        cpadapter = queryAdapter(self.portal, ICanonicalPath)
        newcp = self.portal_cp + '/new_portal_canonical'

        cpadapter.canonical_path = newcp
        prop = self.portal.getProperty(PROPERTY_PATH, None)
        self.assertTrue(prop == newcp,
            "Canonical path adapter setter NOT SET new '%s' value to '%s' " \
            "propery for the portal" % (newcp, PROPERTY_PATH) )

        self.assertTrue(cpadapter.canonical_path == newcp,
            "Canonical path adapter GET '%s' canonical_path, for portal, " \
            "must be: '%s'" % (cpadapter.canonical_path, newcp) )


    def testSet4AT(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        newcp = self.mydoc_cp + '/new_mydoc_canonical'

        cpadapter.canonical_path = newcp
        prop = self.my_doc.getProperty(PROPERTY_PATH, None)
        self.assertTrue(prop == newcp,
            "Canonical path adapter setter NOT SET new '%s' value to '%s' " \
            "propery for the Document" % (newcp, PROPERTY_PATH) )

        self.assertTrue(cpadapter.canonical_path == newcp,
            "Canonical path adapter GET '%s' canonical_path, for Document, " \
            "must be: '%s'" % (cpadapter.canonical_path, newcp) )


    def testValidationWrong(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        for wrong in ['new\nline','s p a c e','with\ttabs']:
            try:
                cpadapter.canonical_path = wrong
            except InvalidValue:
                continue
            else:
                raise self.failureException, "InvalidValue not raised when " \
                      "'%s' wrong value try to set" % wrong
        
    def testValidationGood(self):
        cpadapter = queryAdapter(self.my_doc, ICanonicalPath)
        for good in ['./good','../good','/good', 'good']:
            cpadapter.canonical_path = good


    def testDeleteProperty(self):
        hasprop = self.portal.hasProperty
        cpadapter = queryAdapter(self.portal, ICanonicalPath)
        cpadapter.canonical_path = '/new_portal_canonical'
        assert hasprop(PROPERTY_PATH)

        del cpadapter.canonical_path
        self.assertFalse(hasprop(PROPERTY_PATH),
            "Not deleted Canonical path customization property for the portal")


    def testDelCustomization(self):
        cpadapter = queryAdapter(self.portal, ICanonicalPath)
        cpadapter.canonical_path = '/new_portal_canonical'
        assert cpadapter.canonical_path == '/new_portal_canonical'

        del cpadapter.canonical_path
        self.assertTrue(cpadapter.canonical_path == self.portal_cp,
            "After deleted Canonical path customization property not set to "
            "default value for the portal")


class TestDefaultCanonicalLinkAdapter(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.purl = getToolByName(self.portal, 'portal_url')
        self.my_doc = makeContent(self.portal, portal_type='Document', id='my_doc')
        self.logout()

        self.mydoc_cl = self.my_doc.absolute_url()

    def testRegistration4Portal(self):
        cladapter = queryAdapter(self.portal, ICanonicalLink)
        self.assertFalse(cladapter is None,
            "Can't get canonical link adapter for the plone site object")

    def testRegistration4AT(self):
        cladapter = queryAdapter(self.my_doc, ICanonicalLink)
        self.assertFalse(cladapter is None,
            "Can't get canonical link adapter for the Document object")
        

    def testGetDefault4Portal(self):
        cladapter = queryAdapter(self.portal, ICanonicalLink)
        self.assertTrue(cladapter.canonical_link == self.purl(),
            "Canonical link adapter return '%s' for portal, must be: '%s'" % (
            cladapter.canonical_link, self.purl()) )


    def testGetDefault4AT(self):
        cladapter = queryAdapter(self.my_doc, ICanonicalLink)
        self.assertTrue(cladapter.canonical_link == self.mydoc_cl,
            "Canonical link adapter return '%s' for document, must be: '%s'" % (
            cladapter.canonical_link, self.mydoc_cl) )


    def testSet4Portal(self):
        cladapter = queryAdapter(self.portal, ICanonicalLink)
        newcl = self.purl() + '/new_portal_canonical'

        cladapter.canonical_link = newcl
        prop = self.portal.getProperty(PROPERTY_LINK, None)
        self.assertTrue(prop == newcl,
            "Canonical link adapter setter NOT SET new '%s' value to '%s' " \
            "propery for the portal" % (newcl, PROPERTY_LINK) )

        self.assertTrue(cladapter.canonical_link == newcl,
            "Canonical link adapter GET '%s' canonical_link, for portal, " \
            "must be: '%s'" % (cladapter.canonical_link, newcl) )


    def testSet4AT(self):
        cladapter = queryAdapter(self.my_doc, ICanonicalLink)
        newcl = self.mydoc_cl + '/new_mydoc_canonical'

        cladapter.canonical_link = newcl
        prop = self.my_doc.getProperty(PROPERTY_LINK, None)
        self.assertTrue(prop == newcl,
            "Canonical link adapter setter NOT SET new '%s' value to '%s' " \
            "propery for the Document" % (newcl, PROPERTY_LINK) )

        self.assertTrue(cladapter.canonical_link == newcl,
            "Canonical link adapter GET '%s' canonical_link, for Document, " \
            "must be: '%s'" % (cladapter.canonical_link, newcl) )

    def testValidationWrong(self):
        cladapter = queryAdapter(self.my_doc, ICanonicalLink)
        for wrong in ['http://new\nline','s p a c e','with\ttabs']:
            try:
                cladapter.canonical_link = wrong
            except InvalidValue:
                continue
            else:
                raise self.failureException, "InvalidValue not raised when " \
                    "'%s' wrong value try to set" % wrong
        
    def testValidationGood(self):
        cladapter = queryAdapter(self.my_doc, ICanonicalLink)
        for good in ['http://', './good','../good','/good', 'good']:
            cladapter.canonical_link = good


    def testDeleteProperty(self):
        hasprop = self.portal.hasProperty
        cladapter = queryAdapter(self.portal, ICanonicalLink)
        cladapter.canonical_link = '/new_portal_canonical'
        assert hasprop(PROPERTY_LINK)

        del cladapter.canonical_link
        self.assertFalse(hasprop(PROPERTY_LINK),
            "Not deleted Canonical link customization property for the portal")


    def test_DelCustomization(self):
        cladapter = queryAdapter(self.portal, ICanonicalLink)
        cladapter.canonical_link = '/new_portal_canonical'
        assert cladapter.canonical_link == '/new_portal_canonical'

        del cladapter.canonical_link
        self.assertTrue(cladapter.canonical_link == self.purl(),
            "After deleted Canonical link customization property not set to "
            "default value for the portal")

##
## Dummy object for converter tests
##
class PortalURL:
    def __call__(self):
        return "http://nohost/plone"
    def getRelativeContentPath(self, context):
        return ("plone", context.getId())

class BaseItem:
    portal_url = PortalURL()

    def __init__(self, id):
        self.id = id

    def getId(self):
        return self.id

    def absolute_url(self):
        return self.portal_url() + '/'+ self.getId()

class GoodItem(BaseItem, PropertyManager, Traversable):
    """Property provider."""

class NotPropertyProviderItem(BaseItem, Traversable):
    """Not property provider."""

class NotAdaptableItem(BaseItem):
    """Not adaptable object."""

class TestConvertor(unittest.TestCase):

    def setUp(self):
        self.convertor = CanonicalConvertor("http://domain.com")

    def test_convertIPathToLink(self):
        item = GoodItem("item")
        item._setProperty(PROPERTY_PATH, "/www/some/path")
        self.convertor.convertIPathToLink(item)
        # 1. check canonical link in result object
        result = ICanonicalLink(item).canonical_link
        expect = "http://domain.com/www/some/path"
        self.assertEqual(result, expect, "Got %s canonical link, " \
                         "expect: %s" % (result, expect))
        # 2. canonical path propery mast be delete from the object
        self.assertEqual(item.hasProperty(ICanonicalPath(item).prop), False,
                         "canonical path' property not deleted from the object")

    def test_convertPPathToLink(self):
        item = GoodItem("item")
        item._setProperty("custom_property", "/www/some/path")
        self.convertor.convertPPathToLink(item, prop="custom_property")
        # 1. check canonical link in result object
        result = ICanonicalLink(item).canonical_link
        expect = "http://domain.com/www/some/path"
        self.assertEqual(result, expect, "Got %s canonical link, " \
                         "expect: %s" % (result, expect))
        # 2. custom_property mast be deleted from the object
        self.assertEqual(item.hasProperty("custom_property"), False,
                         "custom_property not deleted from the object")

    def test_convertBadItems(self):
        bad = NotPropertyProviderItem("item")
        self.convertor.convertIPathToLink(bad)
        result = self.convertor.getLogs()
        expect = "ERROR: exceptions.AttributeError: " \
                 "NotPropertyProviderItem instance has no attribute 'hasProperty'"
        self.assertEqual(expect in result, True, "Wrong log: %s" % result)

        bad = NotAdaptableItem("item")
        self.convertor.convertIPathToLink(bad)
        result = self.convertor.getLogs()
        expect = "ERROR: zope.component.interfaces.ComponentLookupError: "
        self.assertEqual(expect in result, True, "Wrong log: %s" % result)

    def test_loggingSuccess(self):
        good = GoodItem("item")
        self.convertor.convertIPathToLink(good)
        result = self.convertor.getLogs()
        expect = "SUCCESS"
        self.assertEqual(expect in result, True, "Wrong log: %s" % result)

    def test_loggingGet(self):
        # log must collect new errors
        # and return full log anytime
        bad = NotPropertyProviderItem("item")
        self.convertor.convertIPathToLink(bad)
        logs = self.convertor.getLogs()
        logs2 = self.convertor.getLogs()
        assert logs != ""
        self.assertEqual(logs == logs2, True,
             "logs not equal: \"%s\" != \"%s\"" % (logs, logs2))
        self.convertor.convertIPathToLink(bad)
        logs3 = self.convertor.getLogs()
        self.assertEqual(logs3 > logs2, True,
             "Log was not updated - last: \"%s\", previous: \"%s\"" % (logs3, logs2))
        
    def test_loggingCleanup(self):
        bad = NotPropertyProviderItem("item")
        self.convertor.convertIPathToLink(bad)
        assert self.convertor.getLogs() != ""
        self.convertor.cleanupLogs()
        logs = self.convertor.getLogs()
        self.assertEqual(logs, "", "Log not cleand-up: \"%s\"" % logs)


class TestAdaptersRegistration(unittest.TestCase):
    """Test of default adapters registration."""

    def setUp(self):
        self.cant = "Can't get \"%s\" adapter for object, which implement: "
        self.doget = "Get \"%s\" adapter for object, which implement: "

    def test_PropertyManagerAndTraversable(self):
        class ProperyAndTraverseProvider(BaseItem, PropertyManager, Traversable):
            """Property and Traversable provider."""
        item = ProperyAndTraverseProvider("test")
        self.assertNotEqual(queryAdapter(item, ICanonicalLink), None,
           self.cant % ICanonicalLink.__name__ + "IPropertyManager and ITraversable.")
        self.assertNotEqual(queryAdapter(item, ICanonicalPath), None,
           self.cant % ICanonicalPath.__name__ + "IPropertyManager and ITraversable.")

    def test_Traversable(self):
        """Traversable enough for get adapter"""
        class TraverseProvider(BaseItem, Traversable):
            """Only Traversable provider."""
        item = TraverseProvider("test")
        self.assertNotEqual(queryAdapter(item, ICanonicalLink), None,
           self.cant % ICanonicalLink.__name__ + "only ITraversable.")
        self.assertNotEqual(queryAdapter(item, ICanonicalPath), None,
           self.cant % ICanonicalPath.__name__ + "only ITraversable.")

    def test_PropertyManager(self):
        """Implementing only IPropertyManager - not enough, because of
           the default value need ITraversable.
        """
        class PropertyManagerProvider(BaseItem, PropertyManager):
            """Only PropertyManager provider."""
        item = PropertyManagerProvider("test")
        self.assertEqual(queryAdapter(item, ICanonicalLink), None,
           self.doget % ICanonicalLink.__name__ + "only IPropertyManager.")
        self.assertEqual(queryAdapter(item, ICanonicalPath), None,
           self.doget % ICanonicalPath.__name__ + "only IPropertyManager.")

    def test_NotProvider(self):
        class NotProvider(BaseItem):
            """Nor Traversable not PropertyManager provider."""
        item = NotProvider("test")
        self.assertEqual(queryAdapter(item, ICanonicalLink), None,
           self.doget % ICanonicalLink.__name__ + "nor ITraversabe not IPropertyManager.")
        self.assertEqual(queryAdapter(item, ICanonicalPath), None,
           self.doget % ICanonicalPath.__name__ + "nor ITraversabe not IPropertyManager.")


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestIndexerRegistration),
        unittest.makeSuite(TestDefaultCanonicalPathAdapter),
        unittest.makeSuite(TestDefaultCanonicalLinkAdapter),
        unittest.makeSuite(TestConvertor),
        unittest.makeSuite(TestAdaptersRegistration),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
