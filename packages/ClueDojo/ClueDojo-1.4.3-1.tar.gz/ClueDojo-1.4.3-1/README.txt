.. -*-rst-*-

============
Introduction
============

ClueDojo is three things:

  1. a Python egg packaging of the Dojo_ Javascript toolkit

  2. a WSGI app to serve the Dojo_ toolkit files

  3. a simple API for accessing the Dojo_ files


.. _Dojo: http://www.dojotoolkit.org


Example Usage
=============

See ``src/cluedojo/demoapp.py`` for an example of how to mount the WSGI component
of ClueDojo.


API Usage
=========

The API is only provided as a convenience for a HTML snippet that includes
necessary dojo files.  It is not required for using the Dojo files themselves.

Example::

  import cluedojo
  headerhtml = cluedojo.get_google_cdn_block()


Credits
=======

Created and maintained by Rocky Burt <rocky@serverzen.com>.
