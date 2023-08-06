Introduction
============

This is yet another social bookmarking viewlet based on
http://www.addthis.com/
Why a new one and not for example `collective.addthis`_?  Well,
probably just because it is so easy to generate the javascript with
the services we choose, and register this as a viewlet.  We did that
for our own `Zest Software`_ site and a client wanted the same, but
then with s checkbox per page to turn it on or off.


Features
========

- This gives you a viewlet near the bottom of the page with links to
  share this on LinkedIn, Twitter or Google; you can share on some other
  sites in a popup; plus a print button.

- Also, you get an extra boolean field ``show_social_viewlet`` on the
  edit page (the Settings tab) of content types (using
  archetypes.schemaextender).  When this field is checked, the viewlet
  is shown.  By default the field is not checked, so the viewlet is
  not shown.

- The extra field and the viewlet are only available when
  you have actually installed this Add-On in your Plone Site (this is
  done using plone.browserlayer).  So when your Zope instance has more
  than one Plone Site, the viewlet is only used in the site where you
  install it.

.. _`collective.addthis`: http://pypi.python.org/pypi/collective.addthis
.. _`Zest Software`: http://zestsoftware.nl
