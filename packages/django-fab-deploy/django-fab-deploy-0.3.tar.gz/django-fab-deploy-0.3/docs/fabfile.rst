fabfile.py API
==============

Overview
--------

* Write a function populating :attr:`env.hosts` and :attr:`env.conf` for
  each server configuration.
* Call :func:`update_env() <fab_deploy.utils.update_env>` at the end of
  each function.
* In order to specify configuration the fab commands should use, run the
  configuring function as a first fab command::

      fab my_site mysql_install

* In order to make configuration default call the configuring function at
  the end of :file:`fabfile.py`::

      from fab_deploy import *

      def my_site():
          env.hosts = ['my_site@example.com']
          # ...

      my_site()

  This way it'll be possible to run fab commands omitting the config name::

      fab mysql_install


Configuring
-----------

.. autofunction:: fab_deploy.utils.update_env


.. attribute:: env.hosts

    A list with host string. Example::

       env.hosts = ['user@example.com']

    See `fabric docs <http://docs.fabfile.org/1.0a/usage/execution.html#hosts>`_
    for explanation.

    User obtained from this string will be used for ssh logins and
    as a default value for :attr:`env.conf.INSTANCE_NAME`.

    .. note::

        multiple hosts are supported via multiple config functions, not
        via this option.

    .. warning::

        Due to bug in Fabric please don't use ``env.user`` and ``env.port``.
        Put the username and non-standard ssh port directly into host string.

.. attribute:: env.conf

    django-fab-deploy server configuration.

    All :attr:`env.conf` keys are available in config templates as
    jinja2 template variables.

.. attribute:: env.conf.INSTANCE_NAME

    Project instance name. It equals to username obtained from :attr:`env.hosts`
    by default. INSTANCE_NAME should be unique for server. If there are
    several sites running as one linux user, set different
    INSTANCE_NAMEs for them.

.. attribute:: env.conf.SERVER_NAME

    Site url for webserver configs. It equals to the first host from
    :attr:`env.hosts` by default.

.. attribute:: env.conf.DB_NAME

    Database name. It equals to :attr:`env.conf.INSTANCE_NAME` by default.

.. attribute:: env.conf.DB_USER

    Database user. It equals to 'root' by default.

.. attribute:: env.conf.DB_PASSWORD

    Database password.

.. attribute:: env.conf.PROCESSES

    The number of mod_wsgi daemon processes. It is a good idea to set it
    to number of processor cores + 1 for maximum performance or to 1 for
    minimal memory consumption. Default is 1.

.. attribute:: env.conf.THREADS

    The number of mod_wsgi threads per daemon process. Default is 15.

    .. note::

        Set :attr:`env.conf.THREADS` to 1 and :attr:`env.conf.PROCESSES` to
        a bigger number if your software is not thread-safe (it will
        consume more memory though).

.. attribute:: env.conf.OS

    A string with server operating system name. Supported operating systems:

    * lenny
    * squeeze

    Default is 'lenny'.

    .. warning::

        Make sure this option is set properly. Deployment will fail with
        incorrect value.

.. attribute:: env.conf.HG_BRANCH

    Named hg branch that should be active on server. Default is "default".
    This option can be used to have 1 repo with several named branches and
    run different servers from different branches.

.. attribute:: env.conf.APACHE_PORT

    The port used by apache backend. It is managed automatically
    and shouldn't be set manually.

You can put any other variables into the :attr:`env.conf`.
They will be accessible in config templates as template context variables.

Writing custom commands
-----------------------

While django-fab-deploy commands are just `Fabric <http://fabfile.org/>`_
commands, there are some helpers to make writing them easier.

.. autofunction:: fab_deploy.utils.inside_project

.. autofunction:: fab_deploy.utils.run_as
