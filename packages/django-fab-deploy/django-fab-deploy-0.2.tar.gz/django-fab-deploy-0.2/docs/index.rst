.. django-fab-deploy documentation master file, created by
   sphinx-quickstart on Fri Feb  4 18:39:09 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-fab-deploy's documentation!
=============================================

django-fab-deploy is a collection of `fabric`_ scripts for deploying and
managing django projects on Debian servers.

Design overview
---------------

* django projects are isolated with `virtualenv`_;
* requirements are managed using `pip`_;
* server interactions are automated and repeatable
  (the tool is `fabric`_ here);
* projects are stored in `mercurial`_ SCM (support for git and rsync
  would be nice).

Server software:

* the OS is Debian Lenny (support for Debian Squeeze is planned);
* the project is deployed with `Apache`_ + `mod_wsgi`_ for backend and
  `nginx`_ in front as a reverse proxy;

Several projects can be deployed on the same VPS using django-fab-deploy.
One project can be deployed on several servers. Projects are isolated and
deployments are repeatable.

.. _virtualenv: http://virtualenv.openplans.org/
.. _pip: http://pip.openplans.org/
.. _fabric: http://fabfile.org/
.. _mercurial: http://mercurial.selenic.com/
.. _Apache: http://httpd.apache.org/
.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _nginx: http://nginx.org/

.. toctree::
   :maxdepth: 2

   guide
   fabfile
   reference
   related

.. toctree::
   :maxdepth: 1

   CHANGES

.. note::

    django-fab-deploy is still at early stages of development and API may
    change in future.


License
=======

Licensed under a MIT license.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

