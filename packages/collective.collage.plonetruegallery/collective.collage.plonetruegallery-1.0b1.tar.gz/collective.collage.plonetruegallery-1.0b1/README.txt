Introduction
============

This product allows to re-use a Gallery view (from
collective.plonetruegallery_) of a Collection in a Collage_.

Installation
============

Add to buildout.cfg::
    
    eggs +=
        collective.collage.plonetruegallery

No further configuration is required.

Usage
=====

First, configure the collective.plonetruegallery_ behaviour: Set the default
view of a Collection to "Gallery View", and configure it.

Next, in the Collage's "Compose" view, "browse" to that Collection. When it is
added to the Collage, select the "gallery-view" layout.

Compatibility
=============

Tested with:

* Plone 4.0
* Products.Collage 1.3
* collective.plonetruegallery >= 1.0.2

.. _collective.plonetruegallery: http://www.plone.org/products/plone-true-gallery
.. _Collage: http://www.plone.org/products/collage

