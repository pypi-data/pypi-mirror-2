.. quantumcore.assets documentation master file, created by
   sphinx-quickstart on Thu Mar 25 14:48:57 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to quantumcore.assets
=============================

`quantumcore.assets` is an asset manager for Python. It allows to store arbitrary files along with some metadata and to retrieve them again. You can choose from different file storage backend such as filesystem, GridFS, S3 and potentially more and from different metadata storages.



Contents:

.. toctree::
   :maxdepth: 2


Getting started
===============

Here is a quick introduction on how to use it.

First you have to initialize a file and a metadata storage as well as the asset manager::

    filestorage = FilesystemStorage(id_template="/%Y/%m/%n")
    mdstorage = MongoDBStorage()
    am = AssetManager(filestorage, mdstorage)
    
Now we assume that somebody has uploaded a file to your web server and you want to store it. Assuming you have a file like object as ``fp``, the ``filesize`` and the ``filename`` you can do that the following way::

    asset = Asset(fp, asset_id=filename)
    
Additionally you can store metadata with that asset::

    asset.blogpost_id = 66542

Now you can store this asset in the asset manager::

    asset_id = am.add(asset)
    
The ``asset_id`` is the finally chosen id as it can be different from the (optional) one you passed in in case there already was an asset with the same id.
    

Retrieving assets by id
-----------------------

Assuming you have the ``asset_id`` stored somewhere you can simply retrieve an asset like this::

    asset = am[asset_id]
    
This will return an ``Asset`` instance which you can use like this::

    fp = asset.file # get a file like object
    asset_id = asset.asset_id
    blogpost_id = asset.blogpost_id # retrieve some metadata passed in on add
    

Searching for assets
--------------------

Imagine you have some image galleries and want to list the images in those galleries. We assume that you have stored some metadata element ``gallery_id`` with those assets to be able to group them by gallery. 

Retrieving all images for gallery ``gallery1`` works as follows::

    images = am.search(gallery_id=u"gallery1")
    
which gives you a list of ``Asset`` instances. 

You can also just retrieve the metadata associated with it::

    images = am.searchmd(gallery_id=u"gallery1")
    
which returns a list of dictionaries. Each will contain an item with the key ``asset_id`` which you can use to retrieve the actual image.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

