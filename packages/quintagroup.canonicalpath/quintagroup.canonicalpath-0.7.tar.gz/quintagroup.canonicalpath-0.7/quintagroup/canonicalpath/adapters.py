import re
from zope.interface import implements
from zope.component import adapts
from zope.schema.interfaces import InvalidValue

from OFS.interfaces import ITraversable
from OFS.interfaces import IPropertyManager

from Products.CMFCore.utils import getToolByName

from quintagroup.canonicalpath.interfaces import ICanonicalPath
from quintagroup.canonicalpath.interfaces import ICanonicalLink

PROPERTY_PATH = "canonical_path"
PROPERTY_LINK = "canonical_link"

_is_canonical = re.compile(
    r"\S*$"               # non space and no new line(should be pickier)
    ).match


class DefaultPropertyAdapter(object):
    """Generic property adapter.
    """
    adapts(IPropertyManager)

    prop = None

    def __init__(self, context):
        self.context = context

    def getDefault(self):
        """Return default value for the self.prop"""
        raise NotImplementedError()

    def getProp(self):
        """ First of all return value from the self.prop,
        if self.prop not exist - return default value
        """
        if self.context.hasProperty(self.prop):
            return self.context.getProperty(self.prop)

        return self.getDefault()

    def setProp(self, value):
        """ First validate value, than add/updater self.prop
        """
        if self.context.hasProperty(self.prop):
            self.context._updateProperty(self.prop, value)
        else:
            self.context._setProperty(self.prop, value, type="string")

    def delProp(self):
        """ Delete self.prop customization
        """
        if self.context.hasProperty(self.prop):
            self.context.manage_delProperties(ids=[self.prop,])


class DefaultCanonicalAdapter(DefaultPropertyAdapter):
    """Generic canonical adapter.
       Add validation support to functionality of DefaultPropertyAdapter.
    """
    adapts(ITraversable)

    def _validate(self, value):
        value.strip()
        if not _is_canonical(value):
            raise InvalidValue(value)
        return value

    def setProp(self, value):
        """ First validate value, than add/updater self.prop
        """
        value = self._validate(value)
        super(DefaultCanonicalAdapter, self).setProp(value)


class DefaultCanonicalPathAdapter(DefaultCanonicalAdapter):
    """Adapts base content to canonical path.
    """
    implements(ICanonicalPath)

    prop = PROPERTY_PATH

    def __init__(self, context):
        super(DefaultCanonicalPathAdapter, self).__init__(context)
        self.purl = getToolByName(self.context,'portal_url')

    def getDefault(self):
        return '/'+'/'.join(self.purl.getRelativeContentPath(self.context))

    canonical_path = property(DefaultCanonicalAdapter.getProp,
                              DefaultCanonicalAdapter.setProp,
                              DefaultCanonicalAdapter.delProp)


class DefaultCanonicalLinkAdapter(DefaultCanonicalAdapter):
    """Adapts base content to canonical link.
    """
    implements(ICanonicalLink)

    prop = PROPERTY_LINK

    def getDefault(self):
        return self.context.absolute_url()

    canonical_link = property(DefaultCanonicalAdapter.getProp,
                              DefaultCanonicalAdapter.setProp,
                              DefaultCanonicalAdapter.delProp)
