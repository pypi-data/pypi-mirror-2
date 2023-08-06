ulif.pynotify -- Watch for filesystem changes
*********************************************

Scan filesystems and look for changes.

Basically, a package that provides an API and scripts to scan parts of
a filesystem for changes. The changes are returned as Python objects
(API) or output on commandline.

While `ulif.pynotify` itself is pure Python, some extensions (notably
the SQLite support) require C extensions.

.. warning:: This package is in a really early state!!!

`ulif.pynotify` will make use of specialized filesystem watchdogs
depending on the OS used, but right now it only contains a simple
Python-only implementation.

For this purpose the package provides a library and a script to detect
filechanges. For 'remembering' file states `ulif.pynotify` provides
SQLite support. 

Documentation
=============

The full package documentation can be found at:

http://packages.python.org/ulif.pynotify


Prerequisites
=============

`ulif.pynotify` is currently tested on Linux only.

* you need Python >= 2.4

* for full install (includung tests etc.) you also need the Python
  header files and a working C-compiler like `gcc`.

Installing the Library
======================

Use `easy_install` to install the library.

Or download the sources and in the root dir of the extracted package
do::

  $ python setup.py install

You might need superuser permissions to do that.


Installing for Development
==========================

After downloading and extracting the sources, in the root dir of the
downloaded file tree do::

  $ python bootstrap/bootstrap.py

which will configure the package for your system. Then, run::

  $ ./bin/buildout

which will generate all scripts needed for development in the local
``bin/`` directory.

Running Tests
-------------

Afterwards you can run the tests by doing::

  $ ./bin/test

Creating Docs
-------------

`ulif.pynotify` comes with some documentation in the ``docs/``
folder. It can be turned into `Sphinx` based HTML by running::

  $ ./bin/make-docs

The docs then can be found in ``docs/_build/html``.

Creating Coverage Reports
-------------------------

We try to keep `ulif.pynotify` at a 100%-test-covered level. You can
do the coverage report by issuing on the command line::

  $ ./bin/coverage-detect
  $ ./bin/coveragereport

This will create HTML docs of the test coverage of each module.
