===================
Distributing Gerald 
===================

Introduction
============

This document describes all of the steps to be followed when packaging and releasing a version of gerald.

Checking the Code
=================

In a working copy (checked out from Subversion) first run pychecker::

    $ pychecker gerald/*.py

Then when you have fixed all of the errors and looked at each of the warnings we bring out pylint::

    $ pylint gerald

For pylint we need to make sure that we use the appropriate configuration file. The only change from the standard I've made to mine is to add the following line::

    disable-msg=W0403,R0903,W0621

Tidying the Code
================

Set Logging Level
-----------------

When developing I set the logging level to 'DEBUG', before distribution set this to 'WARNING'. Open ``schema.py`` and comment out the line that says::

    LOG = get_log('gerald', LOG_FILENAME, 'WARNING')

Make sure that any other line starting ``LOG =`` is commented out.

Update the Documentation
========================

Generating the Documentation
----------------------------

This project uses Sphinx_ for documentation. You will need to have it installed before generating the documentation.

.. _Sphinx: http://sphinx.pocoo.org

First review and update each of the ``.rst`` files in the ``docs`` directory. Then in a working copy of the source code cd to the ``docs`` directory and simply type::

    $ make html

This will generate the project documentation in html format in the ``docs/_build/html`` directory. Copy that directory to the project web site::

    $ scp -r docs/_build/html andy47@scandium.sabren.com:/home/andy47/web/halfcooked.com/code/gerald/

Creating a PDF version of the documentation (with the appropriate modules installed) is as easy as typing::

    $ make pdf

Releasing the Code
==================

Tag the Release
---------------

First we need to complete all of the prior steps. Then we 'tag' the release.::

    $ svn copy http://halfcooked.svn.sourceforge.net/svnroot/halfcooked/trunk http://halfcooked.svn.sourceforge.net/svnroot/halfcooked/tags/release-<revision number>

Or checkout the whole Subversion repository and then do the copy internally.::

    $ svn checkout https://halfcooked.svn.sourceforge.net/svnroot/halfcooked/ hc-root
    $ cd hc-root
    $ svn copy trunk/ tags/release-<release number>

Packaging the Code
------------------

To send it to PyPI::

    $ python setup.py sdist [ --formats=zip,gztar ] bdist_egg upload
    $ python2.5 setup.py bdist_egg upload

Or to create local copies of the source distribution files::

    $ python setup.py sdist --formats=zip,gztar

To create a .tar.gz and a .zip file.

Upload the Code to SourceForge
------------------------------

Upload the distribution files to SourceForge using their web interface. Log on to the project site at https://sourceforge.net/projects/halfcooked and navigate to the File Manager (Project Admin|File Manager)

Create a new folder under ``gerald`` named for the release. Right click it and select ``Uploads here`` and then upload the source and egg files using the ``Upload file`` link.

Update PyPi
-----------

Send a notification to PYPI of the latest release. In the release directory::

    $ python setup.py register

Increment the version number
----------------------------

Now that the release is complete we can start work on the next version of the code. In the trunk, edit the `__init__.py` file in the gerald module and increment the `__version__` variable appropriately.


----

:Author: `Andy Todd <andy47@halfcooked.com>`_
:Last Updated: Tuesday the 8th of June, 2010.
