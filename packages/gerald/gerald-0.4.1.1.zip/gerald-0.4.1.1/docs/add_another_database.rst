====================================
Adding Support for a Database Engine
====================================

Introduction
============

Gerald currently supports a number of popular relational databases_. The code has been developed in a way that makes it possible to add support for different relational databases.

Adding support for a new database to Gerald is possible, it isn't as simple as I would like, but is possible. The code is organised in a hierarchy of modules;::

    schema.py
      |
      |- mysql_schema.py
      |
      |- oracle_schema.py
      |
      |- postgres_schema.py

With each database catered for by a separate module. To support a new database you simply need to create a new module and add the appropriate classes and methods to it. 

Creating a New Module
=====================

To add support for a different type of database follow these steps;

1. Check out the latest code from Subversion using;::

    $ svn checkout http://halfcooked.svn.sourceforge.net/projects/halfcooked halfcooked

2. cd to the code directory (halfcooked/gerald)

3. Take a copy of either ``mysql_schema.py``, ``postgres_schema.py`` or ``oracle_schema.py`` and call it ``<new db name>_schema.py`` (e.g. ``db2_schema.py``).

4. Open up ``<new db name>_schema.py`` in your favourite editor and take a look to familiarise yourself with the code.

   There should be a number of classes in this module that each inherit from a class with the same name in ``schema.py``. Keeping the names consistent is just a convention in the code, it isn't enforced in any way.

   At the very least you will need implementations of the ``Schema`` and ``Table`` classes. Most modern databases will also need ``View``, ``Trigger`` and ``CodeObject``.

5. Before you make any code changes modify the doc string at the top of the module as well as the ``__author__``, ``__date__`` and ``__version__`` attributes just below it.

6. Replace the _get_xxx methods of any classes in the module. You'll notice that ``mysql_schema.py`` has fairly rudimentary support for the different types of objects you will find in a database whereas ``oracle_schema.py`` covers more possibilities. Its probably best to start with the MySQL sample as this will be easier to adapt, you can then implement other object types as and when you need them. I've documented the attributes each class should have (which should be populated in the _get_xxx method) in the class super types in ``schema.py`` and in :doc:`schema_api`.

.. _databases:

Supported Databases
===================

Gerald currently supports Oracle_, MySQL_, and PostgreSQL_.

.. _Oracle: http://www.oracle.com/
.. _MySQL: http://www.mysql.com/
.. _PostgreSQL: http://www.postgresql.org/

----

:Author: `Andy Todd <andy47@halfcooked.com>`_
:Last Updated: Tuesday the 8th of June, 2010.
