.. Sanity documentation master file, created by
   sphinx-quickstart on Sun Jun 13 21:47:47 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======
Sanity
======
.. currentmodule:: sanity

A quick and simple task manager built for teams in an intranet setting.
It's very simple to use by just about anyone on a team.

**Note**: This is in early stages of development, and may not be particularly
useful to many people.

Quickstart
==========

Assuming you're using a WSGI-compatible web server (for instance, the
`mod_wsgi <http://code.google.com/p/modwsgi/>`_ module for Apache or
`gunicorn <http://gunicorn.org/>`_ with other web servers), you can simply put
the following into a file called `sanity.wsgi` and point your web server to
it:

::

   from sanity import app

More example scripts are available in the `/contrib/` directory.

Links
=====

* `website <http://bitbucket.org/aaront/sanity/>`_
* `documentation <http://packages.python.org/Sanity/>`_

.. API Documentation
.. =================
.. This documentation is automatically generated from the sourcecode. This covers
.. the entire public API (i.e. everything that can be star-imported from
.. `sanity`).
.. 
.. Indices and tables
.. ==================
.. 
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

