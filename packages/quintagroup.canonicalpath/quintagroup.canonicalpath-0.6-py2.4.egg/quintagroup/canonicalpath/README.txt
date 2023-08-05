quintagroup.canonicalpath package brings canonical path calculation 
functionality to Plone. The package allows to define path and/or link 
to the object, which may differ from standard physical path or its URL
in portal.

It's used by such products as quintagroup.seoptimizer (for defining
canonical link of the object) and quintagroup.plonegooglesitemaps (on
google sitemaps generation).

This package is intended for bringing *canonical_path* and/or
*canonical_link* property to any traversable object. For that purpose
it defines ICanonicalPath and ICanonicalLink interfaces, and registers
basic adapters for ITraversable objects.

This package also registers *canonical_path* and *canonical_link* indexes
for possible usage in catalog (ZCatalog).

Default adapters behaviour:

  - *canonical_path* returns path from portal root, i.e. for `/plone/front-page` *canonical_path* will be `/front-page`.
  - *canonical_link* returns absoulute url of the object.