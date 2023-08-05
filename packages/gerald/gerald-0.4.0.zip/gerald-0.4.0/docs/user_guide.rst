=================
Gerald User Guide
=================

Introduction
============

Gerald is a general purpose toolkit for managing and analysing relational database schemas.

Gerald allows you to easily work out the structure of your database and with little effort assess the differences between two (or more) versions of it. Typical uses for gerald would include;

 * Identifying the schema differences between your development and production databases
 * Assisting analysis of the impact of specific data model changes or refactorings
 * Generating valid DDL for a database where none exists
 * Transforming a database schema from one relational database engine to another

Definitions
-----------

A schema is a single logical grouping of database objects usually made up of tables, views and stored code objects (functions and procedures).


Getting Started
===============

To use Gerald you need access to two things; a Python_ interpreter and a database_

Once you have those, follow the installation_ instructions below

Installation
============

There are two ways to install Gerald. 

If you are comfortable with source code tools and the command line you can install from the source package (available from the `download page`_ or the `package page_`). Once you have copied the downloaded file to a suitable location on your machine and unzipped it start up a command line, navigate to the package directory and type; ::

      python setup.py install

The other option is to use `easy_install`_. You will need to start a command line session but all you have to do is type ::

      easy_install gerald

How to use Gerald
=================

To compare the same schema in two Oracle databases start an interactive session and type; ::

    >>> import gerald
    >>> first_schema = gerald.OracleSchema('first_schema', 'oracle:/[username]:[password]@[tns connection]')
    >>> second_schema = gerald.OracleSchema('second_schema', 'oracle:/[2nd username]:[2nd password]@[2nd tns connection]')
    >>> print first_schema.compare(second_schema)

You can display a reader friendly version of your schema like this; ::

    >>> import gerald
    >>> my_schema = gerald.MySQLSchema('schema_name', 'mysql:/[username]:[password]@[hostname]/[catalog name]')
    >>> print my_schema.dump()

You can display an XML representation of your schema like this; ::

    >>> import gerald
    >>> my_schema = gerald.OracleSchema('schema_name', 'oracle:/[username]:[password]@[tns entry]')
    >>> print my_schema.to_xml()

For more information on the available objects and methods take a look at the :doc:`schema_api`

A Note on User Accounts
-----------------------

Different database engines provide different levels of information about schema structures. Not only that but permissions differ depending who is enquiring. Generally speaking Gerald works best with a database account that owns the objects being introspected. In most databases this is the schema owner. 

The code is designed to (mostly) fail gracefully. So if the account details you provide can only see some of the metadata available you should still get the structure of the tables, views and other objects returned but you *may* not get all of the details. 

Your best, and safest, bet is to connect as the account with which the database objects were created. Beware though, of connecting as the database super user (e.g. an account with DBA privilege in Oracle) as you may then collect more information than you expect. For instance, in Oracle a DBA user has access to all of the internal system objects.

Why?
====

I wrote this module because I was looking for a cheap, alright - free, tool with similar functionality to ERWin_ and other commercially available database modelling and management tools.
I didn't find anything so I ended up keeping my data model in an Excel spreadsheet and wrote some scripts to generate my Data Definition Language (DDL) into files. 
The one thing that they didn't do, though, was enable me to easily discover the differences between my model and what was deployed in the various databases we were using. 
So I started writing the code that became this module. 

Of course, by the time it was usable the project was long finished. 
I carried on though, because I'll need the same functionality on my next project and undoubtedly the one after that as well.
As it's fun to share, I'm putting this code up on the internet for anyone to use as they see fit. It is licensed under the 
`BSD License`_ (see LICENSE.txt in the distribution).

Gerald can currently extract and compare schemas, and in future I'm hoping that it will expand to store them as well, taking over from my Excel spreadsheet. 
Given infinite time, I'd hope to expand its capabilities to the level of tools like ERwin_ and `Oracle Designer`_.

Databases
---------

Gerald currently supports Oracle_, MySQL_ and PostgreSQL_. For information on how to add another database engine see :doc:`add_another_database`

.. _Python: http://www.python.org/
.. _database: http://en.wikipedia.org/wiki/Database
.. _Oracle: http://www.oracle.com/
.. _PostgreSQL: http://www.postgresql.org/
.. _MySQL: http://www.mysql.com/
.. _ERWin: http://www3.ca.com/Solutions/Product.asp?ID=260
.. _`BSD License`: http://www.opensource.org/licenses/bsd-license.php
.. _`Oracle Designer`: http://otn.oracle.com/products/designer/index.html
.. _`download page`: http://sourceforge.net/projects/halfcooked/files
.. _`easy_install`: http://peak.telecommunity.com/DevCenter/EasyInstall
