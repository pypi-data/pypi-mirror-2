from zope.interface import Interface

class ICanonicalPath(Interface):
    """canonical_path provider interface
    """

    def canonical_path():
        """Return canonical path for the object
        """
