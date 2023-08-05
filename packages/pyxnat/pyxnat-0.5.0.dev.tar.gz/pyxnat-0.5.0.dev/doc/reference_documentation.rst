==============================
Reference documentation
==============================

.. currentmodule:: pyxnat.restapi


The `Interface` class
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyxnat.restapi.Interface
    :members:
    :inherited-members:

The `ResourceObject` class
~~~~~~~~~~~~~~~~~~~~~~~~~~

All REST resources objects are derived from ResourceObject which contains
the common mechanisms to read and write on the server.

.. autoclass:: pyxnat.restapi.ResourceObject
    :members:


The `CollectionObject` class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Collection of ResourceObjects.

.. autoclass:: pyxnat.restapi.CollectionObject
    :members:


The `Project` class
~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyxnat.restapi.Project
    :members:

The `Subject` class
~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyxnat.restapi.Subject
    :members:

The `Experiment` class
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyxnat.restapi.Experiment
    :members:

The `Scan` class
~~~~~~~~~~~~~~~~

.. autoclass:: pyxnat.restapi.Scan
    :members:

The `Resource` class
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyxnat.restapi.Resource
    :members:

The `File` class
~~~~~~~~~~~~~~~~

.. autoclass:: pyxnat.restapi.File
    :members:

The `CacheManager` class
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyxnat.cachemanager.CacheManager
    :members: __init__, __call__, files, resources, clear

The `SearchManager` class
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyxnat.search.SearchManager
    :members: __call__, types, type_fields, names, get, delete, queries, tables


The `Search` class
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: pyxnat.search.Search
    :members:


