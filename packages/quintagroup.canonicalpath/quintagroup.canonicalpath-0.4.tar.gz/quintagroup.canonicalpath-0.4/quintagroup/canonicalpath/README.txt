quintagroup.canonicalpath Package Readme
========================================

Canonical path serves for possibility to define path, which may be
different from standard Physical path in portal. It's uses by such
products as quintagroup.seoptimizer (for defining canonical url of the
object), quintagroup.plonegooglesitemaps (on google sitemap
generation).

This package intended for bring *canonical_path* property to any
traversable object.  For that it defines ICanonicalPath interface, and
register basic adapter for ITraversable.

Also package register canonical_path indexer for possible usage in
catalog (ZCatalog).

Default adapter return path from portal root, i.e. for
`/plone/front-page` *canonical_path* will be `/front-page`.
