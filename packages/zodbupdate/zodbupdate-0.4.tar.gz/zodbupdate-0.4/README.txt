=============================================================
zodbupdate - Update existing databases to match your software
=============================================================

This package provides a tool that automatically identifies and updates
references from persistent objects to classes that are in the process of being
moved from one module to another and/or being renamed.

If a class is being moved or renamed, you need to update all references from
your database to the new name before finally deleting the old code.

This tool looks through all current objects of your database,
identifies moved/renamed classes and `touches` objects accordingly. It
creates transactions that contains the update of your database (one
transaction every 100000 records).

Having run this tool, you are then free to delete the old code.

.. contents::

Usage
=====

Installing the egg of this tool provides a console script `zodbupdate` which
you can call giving either a FileStorage filename or a configuration file
defining a storage::

    $ zodbupdate -f Data.fs
    $ zodbupdate -c zodb.conf

Detailed usage information is available:

    $ zodbupdate -h

Custom software/eggs
--------------------

It is important to install this egg in an interpreter/environment where your
software is installed as well. If you're using a regular Python installation
or virtualenv, just installing the package using easy_install should be fine.

If you are using buildout, installing can be done using the egg recipe with
this configuration::

    [buildout]
    parts += zodbupdate

    [zodbupdate]
    recipe = zc.recipe.egg
    eggs = zodbupdate
        <list additional eggs here>

If you do not install `zodbupdate` together with the necessary software it
will report missing classes and not touch your database.

Non-FileStorage configurations
------------------------------

You can configure any storage known to your ZODB installation by providing a
ZConfig configuration file (similar to zope.conf). For example you can connect
to a ZEO server by providing a config file `zeo.conf`::

    <zeoclient>
        server 127.0.0.1:8100
        storage 1
    </zeoclient>

And then running `zodbupdate` using:

    $ zodbupdate -c zeo.conf


Pre-defined rename rules
------------------------

Rename rules can be defined using entry points::

    setup(...
          entry_points = """
          [zodbupdate]
          renames = mypackage.mymodule:rename_dict
          """)

Rename rules are dictionaries that map old class names to new class names::

    renames = {'mypackage.mymodule ClassName':
               'otherpackage.othermodule OtherClass'}

As soon as you have rules defined, you can already remove the old
import location mentioned in them.


Packing
-------

The option ``--pack`` will pack the storage on success. (You tell your
users to use that option. If they never pack their storage, it is a good
occasion).


Problems and solutions
----------------------

Your Data.fs has POSKey errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you call `zodbupdate` with ``-f`` and the path to your Data.fs,
records triggering those errors will be ignored.


Your Data.fs is old, have been created with Zope 2 and you get strange errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some special support for an old record format got removed from Python
2.6. Running `zodbupdate` with the Python pickler (``-p Python``) will
load those records and fix them.

This will fix your Data.fs.

You have an another error
~~~~~~~~~~~~~~~~~~~~~~~~~

We recommand to run zodbupdate with ``-v -d -p Python`` to get the
maximum of information.

If you are working on big storages, you can use the option ``-o`` to
re-run `zodbupdate` at a failing record you previously encountered
afterward.
