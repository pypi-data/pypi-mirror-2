================================================================================
frapwings.skels package
================================================================================

:Author:    kazuya kawaguchi <kawakazu80@gmail.com>

.. contents ::

Introduction
--------------------------------------------------------------------------------

This package is skelton libraies that used by Frapwings project.
This package may help your packaing and writing document.


Installation
--------------------------------------------------------------------------------

This package can either be installed from a .egg file using setuptools,
or from the tarball using the standard Python distutils.

If you are installing from a tarball, run the following command as an
administrative user::

    python setup.py install

If you are installing using setuptools, you don't even need to download
anything as the latest version will be downloaded for you
from the Python package index::

    easy_install frapwings.skels

If you already have the .egg file, you can use that too::

    easy_install frapwings.skels-py2.5.egg


Requirement Packages
--------------------------------------------------------------------------------

Install the following package.

- PasetScript
- Cheetah


Usage
--------------------------------------------------------------------------------

Execute the following command::

    paster create -t frapwings_package project.package


License
--------------------------------------------------------------------------------

LGPL license.
Please show the current directory on ``License.txt`` file.


