Introduction
************

:mod:`ulif.pynotify` is a Python package that helps keeping track of
changes in filesystem.

It therefore scans the filesystem starting at a given root and checks
which of the found files were changed.

What does it mean that a file has changed? That depends on the
filesystem scanner you are using. `ulif.pynotify` comes currently with
two different scanners:

#) The **plain scanner** takes a path and a Unix timestamp as argument
   and then scans the given path (and all directories) for files and
   directories that were modified since the time given by the
   timestamp.

#) The **pysqlite scanner** is able to store scan results in an SQLite
   database and can therefore remember on second and further runs,
   which files/directories existed at a given prior point in time,
   which items were added or removed meanwhile.

All scanners can be deployed using the package API or a commandline
script called ``pynotify``.

Use of the API is explained in :ref:`api`.

Installing ``ulif.pynotify``
============================

You can install this package using ``easy_install`` or
``zc.buildout``, optionally deploying virtualenv_.

Requirements
------------

- Python 2.x

- A C compiler like GCC if you want to use ``zc.buildout``.

Using ``zc.buildout``
---------------------

The sources for released versions can be found on
http://pypi.python.org/pypi/ulif.pynotify, the developer sources can
be checked out via subversion_ from
https://svn.gnufix.de/repos/main/ulif.pynotify.

Download the sources and eventually unpack them in a local
directory. Change to that directory. Then, run::

  $ python bootstrap/bootstrap.py
  $ bin/buildout

This will generate scripts and directories in the local directory.

Using ``easy_install``
----------------------

If you don't have ``easy_install`` already installed on your system,
run::

  $ wget http://peak.telecommunity.com/dist/ez_setup.py
  $ python ez_setup.py

This will install ``easy_install`` in your $PATH.

If you're using the system Python you need to perform the latter step
as root user. If you want to install ``easy_install`` without root
access, you can deploy virtualenv_.

Afterwards, run::

  $ easy_install ulif.pynotify

If the package is already installed on your system, you can update to
the latest version by::

  $ easy_install -U ulif.pynotify

``easy_install`` will also install the ``pynotify`` commandline
script.

Using the ``pynotify`` commandline script
=========================================

The ``pynotify`` commandline script gives all options like this::

  $ pynotify --help

If you call the script with a path only, it will display all files
found in the respective directory:

  $ pynotify some_dir
  /path/to/some_dir
  /path/to/some_dir/file1
  /path/to/some_dir/file2

If you call the script with a timestamp (seconds since Unix epoch), it
will display all files modified since then only::

  $ pynotify -t 1285000000 some_dir
  /path/to/some_dir/file1

If call the script with the ``--sqlite`` or ``-s`` option, the results
will be stored in a local SQLite database::

  $ pynotify -s some_dir
  A /path/to/some_dir
  A /path/to/some_dir/file1
  A /path/to/some_dir/file2

Here we get a different output: The script tells us, that these files
were (A)dded at the beginning of each line. This is normal for a first
run on a directory. The following markers can appear:

  +--+---------------------------------------------------+
  |A | file/directory added since last run of pynotify   |
  +--+---------------------------------------------------+
  |M | file/directory modified since last run of pynotify|
  +--+---------------------------------------------------+
  |D | file/directory deleted since last run of pynotify |
  +--+---------------------------------------------------+

Unmodified files are not displayed. The scan results are stored in an
SQLite database file ``pynotify.db`` in the local directory.

When we restart the script with the same options and from the same
location, we normally will get no output until one file is
modified. Afterwards we will see::

  $ pynotify -s some_dir
  M /path/to/some_dir/file1

If a file is deleted, this will also be noticed on further runs::

  $ rm some_dir/file1
  $ pynotify -s some_dir
  D /path/to/some_dir/file1

If we want to make sure a certain database is used in runs, we can
tell so by the ``--dbpath`` option::

  $ pynotify -s --dbpath=/path/to/mydb.db some_dir
  A /path/to/some_dir
  A /path/to/some_dir/file1
  A /path/to/some_dir/file2

If the database does not already exist, it will be created on first
access attempt.
 

.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _subversion: http://subversion.tigris.org/