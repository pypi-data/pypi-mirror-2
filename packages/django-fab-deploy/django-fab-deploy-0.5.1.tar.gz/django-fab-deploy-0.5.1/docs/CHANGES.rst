CHANGES
=======

0.5 (2011-02-23)
----------------

- OS is now auto-detected;
- Ubuntu 10.10 maverick initial support (needs better testing?);
- `fabtest <https://bitbucket.org/kmike/fabtest>`_ package is extracted
  from the test suite;
- improved tests;
- :func:`fab_deploy.system.ssh_add_key` can now add ssh key even
  if is is the first key for user;
- 'print' calls are replaced with 'puts' calls in fabfile commands;
- django management commands are not executed if they are not available.

You'll probably want to remove :attr:`env.conf.OS` option from your fabfile.

If you're planning to deploy existing project to Ubuntu, add
``NameVirtualHost 127.0.0.1:{{ APACHE_PORT }}`` line to the top of your
:file:`config_templates/apache.conf` or delete the templates and run
``django-fab-deploy config_templates`` again.

0.4.2 (2011-02-16)
------------------

- tests are included in source distribution

0.4.1 (2011-02-14)
------------------

- don't trigger mysql 5.1 installation on Lenny

0.4 (2011-02-13)
----------------

- :attr:`env.conf.VCS`: mercurial is no longer required;
- undeploy command now removes virtualenv.

0.3 (2011-02-12)
----------------

- Debian Squeeze support;
- the usage of ``env.user`` is discouraged;
- ``fab_deploy.utils.print_env`` command
- ``fab_deploy.deploy.undeploy`` command
- better ``run_as`` implementation

In order to upgrade from 0.2 please remove any usages of ``env.user`` from the
code, e.g. before upgrade::

    def my_site():
        env.hosts = ['example.com']
        env.user = 'foo'
        #...

After upgrade::

    def my_site():
        env.hosts = ['foo@example.com']
        #...


0.2 (2011-02-09)
----------------

- Apache ports are now managed automatically;
- default threads count is on par with mod_wsgi's default value;
- :attr:`env.conf` is converted to _AttributeDict by :func:`fab_deploy.utils.update_env`.

This release is backwards-incompatible with 0.1.x because of apache port
handling changes. In order to upgrade,

- remove the first line ('Listen ...') from project's
  :file:`config_templates/apache.config`;
- remove APACHE_PORT settings from project's :file:`fabfile.py`;
- run ``fab setup_web_server`` from the command line.

0.1.2 (2011-02-07)
------------------
- manual config copying is no longer needed: there is django-fab-deploy
  script for that

0.1.1 (2011-02-06)
------------------
- cleaner internals;
- less constrains on project structure, easier installation;
- default web server config improvements;
- linux user creation;
- non-interactive mysql installation (thanks Andrey Rahmatullin);
- new documentation.

0.0.11 (2010-01-27)
-------------------
- fab_deploy.crontab module;
- cleaner virtualenv management;
- inside_project decorator.

this is the last release in 0.0.x branch.

0.0.8 (2010-12-27)
------------------
Bugs with multiple host support, backports URL and stray 'pyc' files are fixed.

0.0.6 (2010-08-29)
------------------
A few bugfixes and docs improvements.

0.0.2 (2010-08-04)
------------------
Initial release.
