Manual
++++++

Archiver is a tool that takes a source directory and hardlinks or copies all the
files into an archive based on their SHA1 hash, storing their original paths in
an SQLite database and creating a browsable hardlink copy of the original
structure.

If you have lots of archive copies of the same files you can therefore run
archiver on each of them and it will only store one copy, whilst being able to
re-generate any of them.

Sometimes the directory structure of files gives useful information about their
content that you would like to track. For example, if you were archiving photo
taken by individual members of a group on a dive trip you might want to tag a
particular path with tags such as the event, the person whose photos they are
and that the files are photos. Archiver lets you add the sort of information as
*extras*. The files themselves therefore have all the extra metadata for all
the paths they represent.

The internal implementation is quite simple. You just specify a directory to
contain the archive and it has this structure:

``store``
    ``a4e8``
        Files by SHA1 hash ...
    ``ef2b``
        Files by SHA1 hash ...
    ...
``browse``
    <source1>
        None
            Files and Directories ...
        Version 1
            Files and Directories ...
        Version 2
            Files and Directories ...
    <source2>
        Initial
            Files and Directories ...
        Backup
            Files and Directories ...
        ...
    ...
``paths.db``
``copy_in_progress_<pid>``

The tables the data is stored in in the ``paths.db`` SQLite3 database looks like this:

file

    uid
    source__uid ForeignKey('source.uid')),
    hash        (SHA1)
    path        (never ends in a /)
    modified
    created
    accessed
    owner       (UID)
    group       (GID)
    permission  (no handling of sticky bits)
    size        (in bytes)
    link        (rel path to link to if in same source)

directory

    uid
    path       (always ends in a /)
    modified
    created
    accessed
    owner      (UID)
    group      (GID)
    permission (no handling of sticky bits)

source

    uid
    source
    created

extra
    uid       (represents the uid of the thing having extras added, not the uid of the extra itself, so this is not a primarykey)
    key
    value
    type      (can be "int", "datetime" or "string")


The commands themselves are fully documented. Just run something like this to get help:

::

    python -m archiver.command --help
    python -m archiver.command add --help
    etc

In the near future I may also implement:

``verify --skip-hashes``

    Check that all the files referred to in the metadata really exits.

    If ``--skip-hashes`` isn't present, the SHA1 hashes of all the files are
    checked to see if they are correct. A report of failures will be produced, you
    can then use the ``restore`` command to restore any missing or damaged files.

    WARNING: Missing or damaged files may be a sign of hard disk failure, you may
    want to backup your archive or replace your disk.

``redundancy``

    See which files would need to be backed up again to be able to remove a source or version

``backup --where=  --exclude=  src dst``

    Copy files from a store to another location, ignoring metadata changes other than size which would indicate an error.

Special support for symbolic links
==================================

Directory and file symlinks are both supported by archiver but are handled
slightly differntly. Under linux, symlinks can have owner and group permissions
set, but not file permissions, and you can't set modified or accessed times.
Archiver therefore only sets owner and group attributes on a restored symlink.

Symlinks to directories
-----------------------

When restoring a symlink to a directory from a store, archiver will create the
symlink with *whatever data the original had*. If the original contained a
relative path, the restored version would have a relative path. If that
relative path resolved to something outside the source it may now point to the
wrong object because the path the source restored to is not likely to be the
same as the original. If the original symlink was a hard coded path, it would 
be the same path in the restored versions.

To avoid the risk of any problems you should avoid absolute paths in symlinks
to directories and avoid reltive paths to directories outside the source
itself.

.. note ::

   You would have the same problems with copying and pasting the source
   directory so these issues aren't archiver-specific. I'm just highlighting
   some of the risks associated with symlinks in general.

Symlinks to files
-----------------

If the symlink is a relative path to another file within the source, the
restore will restore the symlink. Otherwise, the restore will restore a *copy
of the original file*. This means data doesn't get lost even if the symlink no
longer resolves in the restored location.

In either case, if you were to ``rsync`` your original source directory to a
restored copy of the same source using archive mode (``-a``), no files would be
transferred in either of these cases. Archiver is therefore at least as good as
``rsync`` in its symlink handling.

To test:
* Absolute symlink for directory and file.
