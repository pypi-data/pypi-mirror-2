=======================
de9im: DE-9IM utilities
=======================

As part of my continuing education about the theory and methods underlying
Shapely, GEOS, JTS, and the OGC's Simple Features specs, I've written a small
package of utilities for working with DE-9IM matrices and patterns:
http://bitbucket.org/sgillies/de9im/. Shapely provides the standard (these are
probably my favorite OGC standards) predicates as geometry class methods::

  >>> from shapely.wkt import loads
  >>> p = loads('POLYGON ((1.0 0.0, 0.0 -1.0, -1.0 0.0, 0.0 1.0, 1.0 0.0))') 
  >>> q = loads('POLYGON ((3.0 0.0, 2.0 -1.0, 1.0 0.0, 2.0 1.0, 3.0 0.0))')
  >>> p.disjoint(q)
  False
  >>> p.intersects(q)
  True
  >>> p.touches(q)
  True

but what if you wanted to test whether the features touched at exactly one
point only? A "side hug", you might say. Instead of computing the intersection
and checking its geometry type, you can use the de9im package to define a
DE-9IM matrix pattern and test it against the relation matrix for the two
features. The `0` in the pattern below requires that the intersection of the
boundaries of the features be a 0-dimensional figure. In other words: a point::

  >>> from de9im import pattern
  >>> side_hug = pattern('FF*F0****')
  >>> im = p.relate(q)
  >>> print im
  FF2F01212
  >>> side_hug.matches(im)
  True

One may also use familiarly named patterns::

  >>> from de9im.patterns import touches
  >>> repr(touches)
  "DE-9IM or-pattern: 'FT*******||F**T*****||F***T****'"
  >>> touches.matches(im)
  True
