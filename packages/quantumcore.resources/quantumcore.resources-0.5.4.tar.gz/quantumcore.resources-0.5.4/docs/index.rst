.. quantumcore.resources documentation master file, created by
   sphinx-quickstart on Sat Dec  5 15:46:39 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

quantumcore.resources
=====================

``quantumcore.resources`` lets you manage your CSS and Javascript resources in web applications. You simply list CSS and JS files and ``quantumcore.resources`` will try to merge, minify and cache control them. Check out the :ref:`intro` for more information on how to use it.

Features
========

* merges resources into clusters to minimize amount of files to load
* compresses resources to save bandwidth
* defines cache keys for easy browser caching
* cache keys change if resources change
* full control over clustering/grouping of resources
* full control over compressing of resources
* lets you define custom processors for resources
* lets you define custom resource types easily
* supports JSON template resources (see the `JSON Template Introduction <http://json-template.googlecode.com/svn/trunk/doc/Introducing-JSON-Template.html>`_)
* builtin WSGI handler
* supports auto-reloading


Contents
========

.. toctree::
   :maxdepth: 2

   intro
   naming
   reloading
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

