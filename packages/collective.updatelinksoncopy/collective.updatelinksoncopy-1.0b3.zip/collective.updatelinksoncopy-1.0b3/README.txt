Introduction
============

A drop in package for Plone that improves the copy and paste operation
of folder structures. Reference fields (e.g. relatedItems) and UID
inline links in text fields are rewritten if they reference any of the
content within the folder structure being copied so that they now link
to the copied content.

Development
===========

the buildout in this package will create a test stub which can be run
with::

  ./bin/test

See the doctests for more information of what this package does.


Credits
=======

Initial development by `Matt Halstead <matt@elyt.com>`__ sponsored by
`Innovationz <http://www.innovationz.org>`__.

Addition of reference field handling by `Matt Halstead <matt@elyt.com>`__ sponsored by
`Informaat <http://www.informaat.nl/>`__.
