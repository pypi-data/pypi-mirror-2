import sys
from types import StringTypes
from logging import NOTSET, DEBUG, INFO, ERROR
from logging import Logger, StreamHandler, Formatter
from StringIO import StringIO
from zope.component import getAdapter
from Acquisition import aq_base, aq_inner

from quintagroup.canonicalpath.interfaces  import ICanonicalPath
from quintagroup.canonicalpath.interfaces  import ICanonicalLink
from quintagroup.canonicalpath.adapters import PROPERTY_LINK
from quintagroup.canonicalpath.adapters import PROPERTY_PATH
from quintagroup.canonicalpath.adapters import DefaultPropertyAdapter

class CanonicalConvertor(object):
    """Convert canonical link to canonical path and vice versa."""

    def __init__(self, portal_url):
        """Create instanse of convertor.
           - *portal_url* (string), add in the front of canonical path property
             value for get canonical link.
           - *logger_name* - name of the logger
        """
        self._initLogger()
        self.portal_url = portal_url

    # General APIs
    def getLogs(self):
        self._inout.flush()
        return self._inout.getvalue()

    def cleanupLogs(self):
        self._inout = StringIO()

    def convertILinkToPath(self, obj):
        """Convert canonical link to canonical path"""
        return self._convert(obj, ICanonicalLink, ICanonicalPath,
                             self._convertL2P)

    def convertIPathToLink(self, obj):
        """Convert canonical path to canonical link"""
        return self._convert(obj, ICanonicalPath, ICanonicalLink,
                             self._convertP2L)

    def convertPLinkToPath(self, obj, prop=PROPERTY_LINK):
        """Convert canonical link, got from the *prop* parameter
           to canonical path.
        """
        return self._convert(obj, prop, ICanonicalPath,
                             self._convertL2P)

    def convertPPathToLink(self, obj, prop=PROPERTY_PATH):
        """Convert canonical path, got from the *prop* parameter
           to canonical link.
        """
        return self._convert(obj, prop, ICanonicalLink,
                             self._convertP2L)

    # Service methods
    def _convert(self, obj, src_iface, dst_iface, converter):
        """Convert canonical from source canonical interface
           to destination canonical interface.

           Return True is successfull, False otherwise.
           Log results in logger.
        """
        src_msg = type(src_iface) in StringTypes and src_iface or src_iface.__name__
        msg = "Migrate %s into %s for %s object: " \
               % (src_msg, dst_iface.__name__, obj.absolute_url())
        try:
            src = self._getOrMakeAdapter(obj, src_iface)
            dst = getAdapter(obj, dst_iface)
            # XXX: Check is this correct work XXX
            obj = aq_base(aq_inner(obj))
            # XXX
            converter(src, dst)
        except Exception:
            import sys
            et, em, etr = map(str, sys.exc_info())
            lev = ERROR
            msg += "ERROR: %s: %s" % (et, em)
        else:
            lev = INFO
            msg += "SUCCESS"
        self._logger.log(lev, msg)
            
        return lev == INFO and True or False
    
    def _getOrMakeAdapter(self, obj, arg):
        """Function return adapter for process of the property.
           Adapter get by interface (if arg is not a string - interface assumed)
           OR if arg is string - adapter created from DefaultCanonicalAdapter.
        """
        if type(arg) in StringTypes:
            adapter = DefaultPropertyAdapter(obj)
            adapter.prop = arg
            return adapter
        else:
            return getAdapter(obj, arg)

    def _convertP2L(self, src, dst):
        """Convert canonical path to canonical link."""
        cpath = src.getProp()
        cpath = cpath.startswith('/') and cpath or '/' + cpath
        dst.canonical_link = self.portal_url + cpath
        src.delProp()

    def _convertL2P(self, src, dst):
        """Convert canonical link to canonical path."""
        raise NotImplementedError(
            "Convertion from canonical link to canonical path not implemented")

    def _initLogger(self):
        self._inout = StringIO()
        handler = StreamHandler(self._inout)
        handler.setLevel(DEBUG)
        formatter = Formatter(fmt="[%(asctime)s]: %(message)s",
                                      datefmt="%H:%M:%S")
        handler.setFormatter(formatter)
        self._logger = Logger("quintagroup.canonicalpath", NOTSET)
        self._logger.addHandler(handler)

