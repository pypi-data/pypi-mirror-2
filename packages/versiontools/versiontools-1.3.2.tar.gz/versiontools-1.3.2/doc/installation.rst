Installation
============

Prerequisites
^^^^^^^^^^^^^

There are no requirements to use core features.

To use the bundle bazaar integration plugin you will need bzrlib. Note that on
Windows, depending on how you installed bzr, the integration plugin might
remain inactive. The most common way of installing bzr on Windows is to bundle
the interpreter and all bzr libraries without affecting your regular pytohn
installation. This method is currently not supported.

To build the documentation from source you will need sphinx.

Installation Options
^^^^^^^^^^^^^^^^^^^^

There are several installation options available:

Using Ubuntu PPAs
-----------------

For Ubuntu 10.04 onward there is a stable PPA (personal package archive):

* ppa:linaro-validation/ppa

To add a ppa to an Ubuntu system use the add-apt-repository command::

    sudo add-apt-repository ppa:linaro-validation/ppa

After you add the PPA you need to update your package cache::

    sudo apt-get update

Finally you can install the package, it is called `python-versiontools`::

    sudo apt-get install python-versiontools


Using Python Package Index
--------------------------

This package is being actively maintained and published in the `Python Package
Index <http://http://pypi.python.org>`_. You can install it if you have `pip
<http://pip.openplans.org/>`_ tool using just one line::

    pip install versiontools


Using source tarball
--------------------

To install from source you must first obtain a source tarball from either pypi
or from `Launchpad <http://launchpad.net/>`_. To install the package unpack the
tarball and run::

    python setup.py install

You can pass ``--user`` if you prefer to do a local (non system-wide) installation.

..  note:: 

    To install from source you will need distutils (replacement of setuptools)
    They are typically installed on any Linux system with python but on Windows
    you may need to install that separately.
