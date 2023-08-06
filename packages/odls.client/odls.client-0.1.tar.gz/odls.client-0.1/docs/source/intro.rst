Installing ``odls.client``
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
http://pypi.python.org/pypi/odls.client, the developer sources can
be checked out via subversion_ from
https://svn.gnufix.de/repos/main/odls.client.

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

  $ easy_install odls.client

If the package is already installed on your system, you can update to
the latest version by::

  $ easy_install -U odls.client

``easy_install`` will also install the ``indexer`` commandline
script.

Using the ``indexer`` commandline script
========================================

The ``indexer`` commandline script gives all options like this::

  $ indexer --help
 

.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _subversion: http://subversion.tigris.org/

