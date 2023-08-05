.. Gerald documentation master file, created by
   sphinx-quickstart on Mon Jun  7 17:57:39 2010.

========================
Gerald the half a schema
========================

A Python Schema Comparison Tool
===============================

Gerald is a general purpose database schema toolkit written in Python_. It can be used for cataloguing, managing and deploying database schemas. It is designed to allow you to easily identify the differences between databases.

You can use Gerald to determine the differences between your development and test environments, or to integrate changes from a number of different developers into your integration database.

You can use Gerald to compare schemas across different database engines (e.g. Oracle_ and MySQL_), you can also use it to produce database agnostic documentation in text or XML.

Gerald is designed from the ground up to support as many popular relational database systems as possible.  
Currently it will document and compare schemas from databases implemented in MySQL_, Oracle_ and PostgreSQL_.
Other databases will be supported in future releases.

Contents
========

.. toctree::
   :maxdepth: 1

   user_guide
   schema_api
   add_another_database
   contributing
   distributing

Links
=====

Everything you need to get and run Gerald is at these links;

- Download the package from the PyPI_ `package page`_
- Download the code from the SourceForge_ `download page`_
- Look at the :doc:`API <schema_api>` that is used throughout the code
- The project issue tracker is at the `trac page`_
- The source code is in the `code repository`_ courtesy of Subversion_. Check out a copy with;

::

    svn checkout http://halfcooked.svn.sourceforge.net/svnroot/halfcooked/tags/release-0.4/gerald/ gerald/

Future Plans 
============

This is release 0.4 of Gerald. It's still alpha code, but I use it all of the time.
Having said that, I'm fairly happy with the current functionality so I will only change it if I absolutely have to, and then usually to extend the features available.
This is a minor release with a few bug fixes, improvements and tidying up of the code. This release also includes a refactoring of the documentation to use Sphinx_. The only major addition is support for Views in MySQL - as long as you are running version 5.1 or later. Full details can be found in the CHANGELOG.txt file provided with the code.

The core function is fairly solid and will support a number of enhancements.
I'm specifically thinking about, but in no particular order;

- Improvements to the comparison algorithms
- `SQL Server`_ support
- SQLite_ support
- Firebird_ support
- `DB2 UDB`_ support
- A proper persistence mechanism for schema models
- Make columns first class objects
- Support the input, storage and retrieval of notes against any object
- A diagramming front end

If anyone has suggestions I'm happy to hear your thoughts. Send an email to `andy47@halfcooked.com <mailto:andy47@halfcooked.com>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. * :ref:`modindex`

----

:Author: `Andy Todd <andy47@halfcooked.com>`_
:Last Updated: Tuesday the 8th of June, 2010.

.. _Python: http://www.python.org/
.. _Agile: http://www.agiledata.org/
.. _MySQL: http://www.mysql.com/
.. _Oracle: http://www.oracle.com/
.. _PostgreSQL: http://www.postgresql.org/
.. _SQLite: http://www.sqlite.org/
.. _`SQL Server`: http://www.microsoft.com/
.. _`DB2 UDB`: http://www.ibm.com/software/data/DB2/
.. _Firebird: http://www.firebirdsql.org/
.. _PyPI: http://pypi.python.org/pypi/
.. _`package page`: http://pypi.python.org/pypi/gerald/
.. _SourceForge: http://sourceforge.net/
.. _`trac page`: http://sourceforge.net/apps/trac/halfcooked/
.. _Subversion: http://subversion.tigris.org/
.. _`code repository`: http://halfcooked.svn.sourceforge.net/viewvc/halfcooked/tags/release-0.4/gerald/
.. _`download page`: http://sourceforge.net/projects/halfcooked/files
.. _Sphinx: http://sphinx.pocoo.org/
