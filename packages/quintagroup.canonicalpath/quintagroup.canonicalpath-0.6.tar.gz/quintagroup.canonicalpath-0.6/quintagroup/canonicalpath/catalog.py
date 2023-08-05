from zope.interface import Interface
from zope.component import queryAdapter

#for compatibility with older plone versions 
try:
    from plone.indexer.decorator import indexer 
    IS_NEW = True
except:
    IS_NEW = False
    class IDummyInterface:pass
    class indexer:

         def __init__(self, *interfaces):
            self.interfaces = IDummyInterface,

         def __call__(self, callable):
             callable.__component_adapts__ = self.interfaces
             callable.__implemented__ = Interface
             return callable
    
from interfaces import ICanonicalPath
from interfaces import ICanonicalLink

@indexer(Interface)
def canonical_path(obj, **kwargs):
    """Return canonical_path property for the object.
    """
    adapter = queryAdapter(obj, interface=ICanonicalPath)
    if adapter:
        return adapter.canonical_path
    return None

@indexer(Interface)
def canonical_link(obj, **kwargs):
    """Return canonical_link property for the object.
    """
    adapter = queryAdapter(obj, interface=ICanonicalLink)
    if adapter:
        return adapter.canonical_link
    return None

#for compatibility with older plone versions 
if not IS_NEW:
    from Products.CMFPlone.CatalogTool import registerIndexableAttribute
    map(registerIndexableAttribute, ('canonical_path', 'canonical_link'),
                                    (canonical_path, canonical_link))
