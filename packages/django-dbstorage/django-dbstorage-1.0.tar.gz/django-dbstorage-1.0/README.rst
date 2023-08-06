``django-dbstorage``
====================

A Django file storage backend for files in the database.


Installing
----------

The easiest way to install ``django-dbstorage`` is to use **pip**::

    pip install django-dbstorage


Quick Start
-----------

In your Django ``settings`` file:

* Add ``'django-dbstorage'`` to ``INSTALLED_APPS``

* Set ``DEFAULT_FILE_STORAGE``to
  ``'django_dbstorage.storage.DatabaseStorage'``

* Set ``MEDIA_ROOT`` and ``MEDIA_URL`` to ``None``.


Serving files
-------------

You must set ``MEDIA_URL`` to a view that will serve the static file.

This is left as an exercise to the reader.


Customizing
-----------

``DatabaseStorage`` takes several options. To customize, subclass
it and use that as ``DEFAULT_FILE_STORAGE``. For instance::

    class MyDatabaseStorage(DatabaseStorage):
        def __init__(self):
            super(MyDatabaseStorage, self).__init__(location='/tmp',
                                                    base_url='/files/',
                                                    uniquify_names=True)
