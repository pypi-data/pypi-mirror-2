Running tests
=============

Preparations
------------

In order to run tests you'll need `VirtualBox`_ 4.x and a configured OS image.
Images should:

* have root user with '123' password
* have openssh server installed

.. note::

    Example VMs:

    * `Lenny.ova (312M) <http://dl.dropbox.com/u/21197464/Lenny.ova>`_
    * `Squeeze.ova (436M) <http://dl.dropbox.com/u/21197464/Squeeze.ova>`_

After you get the image, make sure it is not running and execute the
'preparevm.py' script from fab_deploy_tests folder (pass your VM name)::

    ./preparevm.py Lenny

This command configures port forwarding (127.0.0.1:2222 to guest 22 port,
127.0.0.1:8888 to guest 80 port) and takes 'initial' snapshot used for test
rollbacks (it is taken from booted machine in order to speedup tests).

.. _VirtualBox: http://www.virtualbox.org/

Running
-------

Pass OS name (as for :attr:`env.conf.OS`) and VM name (e.g. Lenny)
to runtests.py script::

    cd fab_deploy_tests
    ./runtests.py <OS name> <VM name or uid>

Tests can take a long time to run because VM is rolled back to clean
state before each test.

In order to get coverage reports, install coverage.py (``pip install coverage``)
and the run::

    cd fab_deploy_tests
    ./runcoverage.sh <OS name> <VM name or uid>

html reports will be placed in ``htmlcov`` folder.

