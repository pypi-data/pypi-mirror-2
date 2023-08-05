from zope.interface import implements
from zope.component import adapts

from OFS.interfaces import ITraversable
from Products.CMFCore.utils import getToolByName

from quintagroup.canonicalpath.interfaces import ICanonicalPath


class canonicalPathAdapter(object):
    """Adapts base content to canonical path.
    """
    adapts(ITraversable)
    implements(ICanonicalPath)

    def __init__(self, context):
        self.context = context

    def canonical_path(self):
        purl = getToolByName(self.context,'portal_url')
        return '/'+'/'.join(purl.getRelativeContentPath(self.context))
