lpdistutils
===========

This is a set of extra commands for distutils/setuptools that allow working with
Launchpad and Bazaar. They are similar to the "register" and "upload" commands
provided by distutils for working with pypi.

Commands
--------

  * lpregister - register the project on Launchpad. This takes the information from
    setup.py and creates you a Launchpad project based on that information.

    In addition, if you are working in a bzr branch then that branch will be pushed
    to Launchpad, and set as the development focus of the new project.

  * lpupload - this uploads a release to Launchpad for you. Similar to the "upload"
    command you run it with the command to build the artefact you wish to upload, e.g.::

      python setup.py --command-packages lpdistutils  sdist lpupload --sign

    If you wish to upload to PYPI too you can do this with::

      python setup.py --command-packages sdist upload --sign lpupload --use-existing-sig

  * bzrtag - this sets a bzr tag based on the version number in setup.py, so you
    can use it as part of your release process.

Usage
-----

You need to tell distutils/setuptools to load the commands provided by lpdistutils, and
you do this with the --command-packages option to setup.py.

::

  python setup.py --command-packaegs lpdistutils

This must be the first thing passed.

It is possible to enable it in the `distutils config files`_

.. _distutils config files: http://docs.python.org/install/index.html#distutils-configuration-files

like::

[global]
command-packages = lpdistutils
