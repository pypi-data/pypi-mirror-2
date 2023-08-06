.. contents::

Introduction
============

``collective.recipe.rsync`` is a ``zc.buildout`` recipe that makes it easy to
synchronize data between two locations, via the ``rsync`` program. 

It was originally created to copy a ``Data.fs`` file between two Plone
environments (i.e. from production to development). But
you can use it to synchronize any data; e.g. ZODB blob files and so on. See
example below.

.. Note::

    ``collective.recipe.rsync`` currently assumes you have a UNIX-based
    operating system and that the ``rsync`` binary is in your path when you
    execute buildout or the rsync script.

Installation
------------

Add a section to your ``buildout.cfg`` file, e.g. ``filestorage``::

    [buildout]
    parts =
        ...
        filestorage

    [filestorage]
    recipe = collective.recipe.rsync
    source = aclark@aclark.net:/srv/aclark/var/filestorage/Data.fs
    target = var/filestorage/Data.fs

Run buildout; you should see:: 

    --------------------------------------------------------------------------------
    Running rsync...
      rsync -av --partial --progress
    aclark@aclark.net:/srv/aclark/var/filestorage/Data.fs
    var/filestorage/Data.fs
      this may take a while!
    ...

Specify alternate SSH port
~~~~~~~~~~~~~~~~~~~~~~~~~~

Optionally, you may specify an alternate SSH port for rsync to use::

    [filestorage]
    recipe = collective.recipe.rsync
    source = aclark@aclark.net:/srv/aclark/var/filestorage/Data.fs
    target = var/filestorage/Data.fs
    port = 22001

Run buildout; you should see:: 

    Running rsync...
      rsync -e 'ssh -p 22001' -av --partial --progress 
    aclark@aclark.net:/srv/aclark/var/filestorage/Data.fs
    var/filestorage/Data.fs
      this may take a while!
    ...

Create a script
~~~~~~~~~~~~~~~

Optionally, you may create a rsync script to execute later. Just configure ``script = true`` like so::

    [rsync]
    recipe = collective.recipe.rsync
    source = sample_input.txt
    target = sample_input_copy.txt
    script = true

Run buildout; you should see:: 

    $ bin/buildout
    ...
    Installing rsync.
    Generated script '/Users/aclark/Developer/collective/collective.recipe.rsync/bin/rsync'.

Notice that rsync no longer runs when you run bin/buildout. Now you may run rsync whenever you like::

    $ bin/rsync 
    --------------------------------------------------------------------------------
    Running rsync...
      rsync -e 'ssh -p None' -av --partial --progress sample_input.txt
    sample_input_copy.txt
      this may take a while!
    building file list ... 
    1 file to consider

    sent 88 bytes  received 20 bytes  216.00 bytes/sec
    total size is 245  speedup is 2.27
    Done.
    --------------------------------------------------------------------------------

Further, you may now consider executing an rsync script automatically via cron
(see: z3c.recipe.usercrontab).

Example
-------

Here is a full example ``database.cfg`` file that demonstrates how to copy a
``Data.fs`` file and ``var/blobstorage`` files::

    [buildout]
    extends = buildout.cfg
    parts += 
        filestorage
        blobstorage

    [filestorage]
    recipe = collective.recipe.rsync
    source = aclark.net:/srv/aclark_net_website/var/filestorage/Data.fs
    target = var/filestorage/Data.fs

    [blobstorage]
    recipe = collective.recipe.rsync
    source = aclark.net:/srv/aclark_net_website/var/blobstorage/
    target = var/blobstorage


Contact
-------

Questions/comments/concerns? Please e-mail: aclark@aclark.net.

