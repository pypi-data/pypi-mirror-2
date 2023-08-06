.. quantumcore.assets documentation master file, created by
   sphinx-quickstart on Thu Mar 25 14:48:57 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to quantumcore.storages
===============================

`quantumcore.storages` is a collection of different storage mechanisms for various kinds
of data such as binary objects (files, images etc.), dictionary like documents and more.

It supports backends like GridFS, S3, MongoDB and others. 


Contents:

.. toctree::
   :maxdepth: 2

   general
   storages/index
   development/index
   
   
   
   
Overview
========

The following storage modules are available:

``quantumcore.storages.MemoryDataStore``::
    a simple store which holds dictionaries in memory.
``quantumcore.storages.FilesystemStore``::
    a store which can save and retrieve files on the filesystem
``quantumcore.storages.ExtendedFileStore``::
    a store which can save files and metadata along with it.
``quantumcore.storages.BundleFileStore``::
    a store which can hold a bundle of files, e.g. different sizes of an image.


Contributors
============

* `Christian Scholz <http://mrtopf.de/blog>`_, `COM.lounge GmbH <http://comlounge.net>`_

Code and bugtracker
===================

The source code and an issue tracker can be found `at bitbucket <http://bitbucket.org/mrtopf/quantumcore.storages>`_.


License 
=======

``quantumcore.storages`` has been released under an MIT license:

.. pull-quote::

    The MIT License

    Copyright (c) 2010 COM.lounge GmbH

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

