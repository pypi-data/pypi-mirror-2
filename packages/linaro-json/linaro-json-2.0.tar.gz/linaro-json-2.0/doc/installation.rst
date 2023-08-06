Installation
============

Prerequisites
^^^^^^^^^^^^^

This package has the following prerequisites:

* simplejson 
* versiontools

To run the test suite you will also need:

* testtools
* testscenarios

To build the documentation from source you will also need:

* sphinx

Installation Options
^^^^^^^^^^^^^^^^^^^^

There are several installation options available:

Using Ubuntu PPAs
-----------------

For Ubuntu 10.04 onward there is a PPA (personal package archive):

* ppa:zkrynicki/lava

This PPA has only stable releases. To add it to an Ubuntu system use the
add-apt-repository command::

    sudo add-apt-repository ppa:zkrynicki/lava

After you add the PPA you need to update your package cache::

    sudo apt-get update

Finally you can install the package, it is called `python-linaro-json`::

    sudo apt-get install python-linaro-json


Using Python Package Index
--------------------------

This package is being actively maintained and published in the `Python Package
Index <http://http://pypi.python.org>`_. You can install it if you have `pip
<http://pip.openplans.org/>`_ tool using just one line::

    pip install linaro-json


Using source tarball
--------------------

To install from source you must first obtain a source tarball from either
`pypi project page <http://pypi.python.org/pypi/linaro-json>`_
or from `Launchpad project page <http://launchpad.net/linaro-python-json>`_.
To install the package unpack the tarball and run::

    python setup.py install

You can pass ``--user`` if you prefer to do a local (non system-wide) installation.

..  note:: 

    To install from source you will need distutils (replacement of setuptools)
    They are typically installed on any Linux system with python but on Windows
    you may need to install that separately.
