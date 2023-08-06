Introduction
============

This package provides portlet that lists blog posts from your wordpress blog.

Overview
--------

``collective.portlet.wordpress`` package adds a new portlet to Plone site
called ``WordPress Blog``. It gives you ability to list blog posts from
wordpress based blog in your Plone site. Portlet makes request to wordpress
blog's rss feed and parses it to get recent blog entries. See below for details about installation and usage of this portlet in your site.


Compatibility
-------------

This add-on was tested for Plone 3 and Plone 4.


Installation
------------

* to add the package to your Zope instance, please, follow the instructions
  found inside the ``docs/INSTALL.txt`` file
* then restart your Zope instance and install the ``Wordpress Blog Portlet``
  package from within the ``portal_quickinstaller`` tool


Portlet Usage
-------------

The ``WordPress Blog`` portlet owns a bunch of fields. Here we explain how it works:

* ``Portlet header``. This string is used in the portlet header. 
* ``Blog url``.  Here you specify the URL to your Wordpress blog root. Note: do not
  add a path to the blog's RSS feed, it is added by the portlet itself.
* ``Request Timeout``. Number of seconds you allow the portlet to wait for a response
  from the Wordpress blog.
* ``Number of entries``. Specifies the number of entries to list in the portlet.
* ``More link``. If checked, '...more' link pointing to the blog will be inserted at
  the bottom of the portlet.


Live Examples
=============

* http://www.roserehab.com/


Credits
=======


Companies
---------

|martinschoel|_

* `Martin Schoel Web Productions <http://www.martinschoel.com/>`_
* `Contact us <mailto:python@martinschoel.com>`_


Authors
-------

* Vitaliy Podoba <vitaliy@martinschoel.com>
* Sergiy Krasovkiy


Contributors
------------


.. |martinschoel| image:: http://cache.martinschoel.com/img/logos/MS-Logo-white-200x100.png
.. _martinschoel: http://www.martinschoel.com/
