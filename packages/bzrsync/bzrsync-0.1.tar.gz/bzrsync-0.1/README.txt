BzrSync - Bazaar repository/branch synchronization tool
=======================================================

BzrSync is a tool to help a developer using Bazaar on multiple machines.
It automatically keeps selected repositories and branches synchronized across
the machines. Bazaar itself is used for the synchronization (with "bzr pull"),
ensuring consistency at all times.

Features
--------

- any number of machines are supported

- consistency is guaranteed at all times

Installation
------------

To install the latest stable version of BzrSync, using pip_:

::

  pip install bzrsync

or using setuptools_:

::

  easy_install bzrsync

Otherwise, if neither pip_ nor setuptools_ are available, it is possible
to download (eg. from PyPI_) the `source`_ package, extract it and run the
usual ``setup.py`` commands:

::

  python setup.py install

.. _pip: http://pypi.python.org/pypi/pip
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _EasyInstall: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _PyPI: http://pypi.python.org/pypi
.. _`source`: http://pypi.python.org/pypi/bzrsync


Help and Development
--------------------

Alternatively, if you'd like to update the software occasionally to pick
up the latest bug fixes and enhancements before they make it into an
offical release, branch from the `Bazaar`_ repository hosted on `LaunchPad`_
instead.
Just follow the procedure outlined below:

1. Make sure that you have `Bazaar`_ installed, and that you can run its
   commands from a shell. (Enter ``bzr help`` at a shell prompt to test
   this.)

2. Create a local branch and working tree from the official one::

    bzr branch lp:bzrsync bzrsync

3. Then from the ``bzrsync`` directory you can run the ``setup.py develop``
   command to install the library in your Python `site-packages` directory
   using a link, which allows to continue developing inside the working tree
   without the need to re-install after every change. See the
   `setuptools development mode`_ documention for more information::

    $ sudo
    # python setup.py develop

.. _`development home page`: https://launchpad.net/bzrsync
.. _`bugs`: https://bugs.launchpad.net/bzrsync
.. _`LaunchPad`: http://launchpad.net
.. _`Bazaar`: http://bazaar-vcs.org/
.. _`changes`: http://bazaar.launchpad.net/~softwarefabrica/bzrsync/trunk/changes
.. _`PYTHONPATH`: http://docs.python.org/tut/node8.html#SECTION008110000000000000000
.. _`junction`: http://www.microsoft.com/technet/sysinternals/FileAndDisk/Junction.mspx
.. _`setuptools development mode`: http://peak.telecommunity.com/DevCenter/setuptools#development-mode


LICENSE
-------

This software is covered by the GNU General Public License version 2.
It is:

    Copyright (C) 2010-2011  Marco Pantaleoni. All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2 as
    published by the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
