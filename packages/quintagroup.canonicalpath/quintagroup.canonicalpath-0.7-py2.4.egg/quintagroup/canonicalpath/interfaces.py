from zope.interface import Interface, Attribute

class ICanonicalPath(Interface):
    """canonical_path provider interface
    """

    canonical_path = Attribute("canonical_path",
        "canonical_path - for the object. Adapter must implement "
        "*setter* and *getter* for the attribute")

class ICanonicalLink(Interface):
    """canonical_link provider interface
    """

    canonical_link = Attribute("canonical_link",
        "canonical_link - for the object. Adapter must implement "
        "*setter* and *getter* for the attribute")

