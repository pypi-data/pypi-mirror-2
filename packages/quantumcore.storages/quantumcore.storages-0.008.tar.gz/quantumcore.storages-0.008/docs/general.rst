==============================
General interface for storages
==============================

All the storages follow (if possible) a generic and easy interface which is described
below.

Adding objects
==============

To add an object to a storage the following method is used::

    obj_id = storage.add(obj)
    
It returns the object id assigned to the object. With some storages you can add additional
parameters like a predefined object id. Note though that this can be overridden by the storage e.g. in case of naming conflicts.

Retrieving objects
==================

To retrieve an object again you need it`s object id and then you can use one of the following ways::

    obj = storage.get(obj_id)
    obj = storage[obj_id]
    
If no object with the given id is given the first method will return None while the latter method will raise a ``KeyError``.


Deleting objects
================

To delete an object again you need the object id and you can do it the following way::

    storage.delete(obj_id)


Updating objects
================

To update an object you do need the object and it's object id::

    storage.update(object, object_id)
    
In some storages you don't need the object id as the object itself will contain the id already but for e.g. a filestorage you need to give the id.


Retrieving all objects
======================

You can also export all content from a storage like follows::

    for object in storage:
        # do something with the object
        
The storage itself is a generator which will return all objects. "Objects" does mean really the object but sometimes it can be a tuple, e.g. in the case of the ``FilesystemStorage`` which returns ``(filename, filepointer)`` tuples.


    





