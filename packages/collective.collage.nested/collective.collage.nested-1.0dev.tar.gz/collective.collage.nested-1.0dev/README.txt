Introduction
============

This package enables `Collage
<http://pypi.python.org/pypi/Products.Collage>`_ to support nested Collage objects.

Additionally, two views (Collage layouts) are available:

* **full**: displays exactly the same as a Collage default view, including
  title, description, related items and, of course, the contents (rows 
  and columns).

* **content**: displays only contents (rows and columns).

To allow Collage objects to be created inside columns we had to patch
``Products.Collage.config.COLLAGE_TYPES`` and remove `Collage` content type
from it.

Additionally, a CSS resource is registered (just below the original 
``collage.css``) to display nested column widths correctly.

Usage
=====

If you want to create new views (layouts) for nested collage objects
base your class on the new ``NestedCollageView`` one, like this::

    from collective.collage.browser.views import NestedCollageView

    class MyNestedCollageView(NestedCollageView):
        """ A custom view for a nested collage """
        ...


Known issues
============

Although ``COLLAGE_TYPES`` is patched, Collage vocabulary
``collage.vocabularies.CollageUserFriendlyTypes`` doesn't seem to learn about
it, so Collage control panel doesn't display ``Collage`` as an allowed
portal type.


