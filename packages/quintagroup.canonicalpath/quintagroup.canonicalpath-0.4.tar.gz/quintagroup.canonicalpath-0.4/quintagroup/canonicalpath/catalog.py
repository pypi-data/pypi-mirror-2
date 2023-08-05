from zope.interface import Interface
from zope.component import queryAdapter
from plone.indexer.decorator import indexer

from interfaces import ICanonicalPath

@indexer(Interface)
def canonical_path(obj, **kwargs):
    """Return canonical_path property for the object.
    """
    cpath = queryAdapter(obj, interface=ICanonicalPath)
    if cpath:
        return cpath.canonical_path()
    return None
