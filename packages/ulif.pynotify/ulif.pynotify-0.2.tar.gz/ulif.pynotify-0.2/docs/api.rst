.. _api:

:mod:`ulif.pynotify` API
************************

Contents:

.. toctree::

   api_base
   api_sqlite
   api_ui

.. module:: ulif.pynotify

.. data:: NONE

   A filechange state.

   Indicates that a file/directory was not modified.

.. data:: ADDED

   A filchange state.

   Indicates that a file/directory was added.

.. data:: MODIFIED

   A filechange state.

   Indicates that a file/directory was modified.

.. data:: DELETED

   A filechange state.

   Indicates that a file/directory was deleted.

.. data:: FILE_TYPE

   Filetype marker.

   Indicates that a filesystem item is a regular file.

.. data:: DIRECTORY_TYPE

   Filetype marker.

   Indicates that a filesystem item is a directory.

.. data:: UNKNOWN_TYPE

   Filetype marker.

   Indicates that a filesystem entity is not a regular file nor a
   directory.

Examples
========

To see how the API works we first create a directory we want to scan
afterwards:

    >>> import os
    >>> import tempfile
    >>> dir = tempfile.mkdtemp()
    >>> samplefile1 = open(os.path.join(dir, 'sample1'), 'wb').write('foo')
    >>> samplefile2 = open(os.path.join(dir, 'sample2'), 'wb').write('bar')

``FSWalker`` -- the plain scanner
---------------------------------

Now we can scan that directory using the plain scanner:

    >>> from ulif.pynotify.base import FSWalker
    >>> walker = FSWalker()
    >>> result = walker.walk(dir, 0)

We told the walker to scan the directory ``dir`` and to look for files
and directories changed since ``0``. The zero is an integer number
representing a Unix timestamp that counts seconds since January 1st,
1970. Timestamps for regular Python datetimes can be retrieved
deploying the Python standard :mod:`datetime` lib.

The result is a generator which keeps usage cheap also for many files:

    >>> result
    <generator object at 0x...>

    >>> result = list(result)
    >>> len(result)
    3

We got three results which means: three files changed since timestamp
begin of epoch. Each result is a
:class:`ulif.pynotify.base.FSChange` object:

    >>> result[0]
    <ulif.pynotify.base.FSChange object at 0x...>

Each change provides an absolute path, the filetype, and a marker to
tell what kind of file we have:

    >>> from ulif.pynotify import MODIFIED, FILE_TYPE
    >>> change0 = result[1]
    >>> change0.path
    '/.../sample1'

    >>> change0.changetype is MODIFIED
    True

    >>> change0.filetype is FILE_TYPE
    True

With the plain scanner all file changes returned have changetype
ulif.pynotify.MODIFIED as the scanner cannot store results and
therefore cannot detect additions and deletions. This is different
with the 'persistent' scanners like sqlite-base scanner.

``SQLiteFSWalker`` -- a persistent scanner
------------------------------------------

The :class:`ulif.pynotify.sqlite.SQLiteFSWalker` scanner stores
results of scans in a SQLite database. It can therefore detect also
additions and deletions of files and directories.

By default the scanner keeps the database in memory, which means that
each such new scanner instance will start with an empty database:

    >>> from ulif.pynotify.sqlite import SQLiteFSWalker
    >>> walker = SQLiteFSWalker()
    >>> results1 = walker.walk(dir)
    >>> results1
    <generator object at 0x...>

As before we get a generator object that provides
:class:`ulif.pynotify.base.FSChange` objects.

Different to the plain scanner, the changes now indicate that the
files were added (as they have not been in the database before):

    >>> from ulif.pynotify import ADDED, DELETED
    >>> results1 = list(results1)
    >>> results1[0].changetype is ADDED
    True

When we restart the run, we will get no modifications at all:

    >>> results = walker.walk(dir)
    >>> len(list(results))
    0

If we touch some file in the searched path and rerun, the scanner will
notice this:

    >>> import os
    >>> samplefile1 = os.path.join(dir, 'sample1')
    >>> samplefile2 = os.path.join(dir, 'sample2')
    >>> os.utime(samplefile1, None)
    >>> results2 = list(walker.walk(dir))
    >>> len(results2)
    1

    >>> results2[0].changetype is MODIFIED
    True

Finally, if we delete the file this will be detected as well on
subsequent runs:

    >>> os.unlink(samplefile1)
    >>> results3 = list(walker.walk(dir))

As deleting files might also modify the containing directory, we
filter the deleted file entry:

    >>> results3 = [x for x in results3 if x.path.endswith('/sample1')]
    >>> results3[0].changetype is DELETED
    True

Using a persistent database
---------------------------

Until now we used the scanner with an in-memory database. That's not
very handy if we have large amounts of data to handle or if we want
the data to be really persistent.

To tell a SQLite walker to write results to a file, we can simply pass the appropriate path as argument:

    >>> dbdir = tempfile.mkdtemp()
    >>> dbpath = os.path.join(dbdir, 'mydatabase.db')
    >>> walker1 = SQLiteFSWalker(dbpath)
    >>> results = walker1.walk(dir)
    >>> len(list(results))
    2

The database was created and filled:

    >>> import os
    >>> os.listdir(dbdir)
    ['mydatabase.db']

.. warning:: The database is written step by step when you request the
          single items of the generator. If you abort retrieving the
          generator data, also the database is **not** updated for the
          items not requested up to that point in time.

          In our example we retrieved the complete generator data by
          using ``list()``.

Now when we create a new walker, we can reuse the database:

    >>> walker2 = SQLiteFSWalker(dbpath)
    >>> results = walker2.walk(dir)
    >>> len(list(results))
    0

We changed no file since the first run. Now we touch one file and scan
the directory again:

    >>> os.utime(samplefile2, None)
    >>> results = walker2.walk(dir)
    >>> results = list(results)
    >>> len(results)
    1

Now we have one change:

    >>> results[0].path
    '/.../sample2'

    >>> results[0].changetype is MODIFIED
    True

Clean up:

    >>> import shutil
    >>> shutil.rmtree(dir)
    >>> shutil.rmtree(dbdir)
