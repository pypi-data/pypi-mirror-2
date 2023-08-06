User Guide
==========

django-fab-deploy is just a collection of scripts. Most of them can be used
independently. The basic workflow for setting up a new web site is
described in this guide. If this workflow doesn't fit for some reason then
django-fab-deploy can still be used as a collection of scripts.

Prerequisites
-------------

1. Clean Debian Lenny (Debian Squeeze supported is planned) server or
   VPS with root ssh access;
2. working ssh key authentication;
3. django project stored in mercurial VCS.

.. warning::

    OpenVZ has serious issues with memory management
    (VIRT is counted and limited instead of RSS) so a lot of software
    (including apache2, Java and mysql's InnoDB engine) is nearly unusable on
    OpenVZ while being memory-wise and performant on XEN/KVM. So please try to
    avoid OpenVZ or Virtuozzo VPS's, use XEN or KVM or real servers.


Prepare the project
-------------------

1. Install django-fab-deploy its requirements::

       pip install django-fab-deploy
       pip install jinja2
       pip install -e git+git://github.com/bitprophet/fabric.git#egg=Fabric-dev

   .. note::

       django-fab-deploy doesn't work with Fabric 0.9.x, Fabric should be installed
       from github repository.

2. Create :file:`fabfile.py` at project root. It should provide one or more
   function putting server details into Fabric environment. Otherwise it's just
   a standart Fabric's fabfile (e.g. project-specific scripts can also be put
   here). Example::

        # my_project/fabfile.py
        from fabric.api import *
        from fab_deploy import *

        def my_site():
            env.hosts = ['example.com']
            env.user = 'example'
            env.conf = dict(
                DB_PASSWORD = 'password',
                SERVER_ADMIN = 'example@example.com',
                APACHE_PORT = 8082,
            )
            update_env()

        my_site()

   In order to make things simple set ``env.user`` to your project name. It
   should be a valid python identifier. Don't worry if there is no such user
   on server, django-fab-deploy can create linux user and setup ssh
   access for you, and it is preferrable to have linux user per
   project if possible.

   .. note::

       There are some defaults, e.g. ``DB_NAME`` equals to ``INSTANCE_NAME``,
       and ``INSTANCE_NAME`` equals to ``env.user``.

3. Copy ``config_templates`` folder from django-fab-deploy to your project root.

   .. note::

       Read the configs and adjust them if it is needed. Basic configs
       are usually a good starting point and should work as-is.

       {{ variables }} can be used in config templates. They will be
       replaced with values from ``env.conf`` on server.
       This also apply for :file:`config.server.py` file.

4. Create :file:`config.server.py` at project root. Example::

        # my_project/config.server.py
        # config file for environment-specific settings

        DEBUG = False
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': '{{ DB_NAME }}',
                'USER': '{{ DB_USER }}',
                'PASSWORD': '{{ DB_PASSWORD }}',
                'HOST': '',
                'PORT': '',
                'OPTIONS': {
                    "init_command": "SET storage_engine=INNODB"
                },
            }
        }
        MEDIA_URL = 'http://{{ SERVER_NAME }}/static/'

   Then create :file:`config.py` for development.
   Import config in project's :file:`settings.py`::

       # Django settings for my_project project.
       # ...
       from config import *
       # ...

   ``config.py`` trick is also known as ``local_settings.py``
   (make sure ``config.py`` is ignored in your ``.hgignore``).


5. Create ``reqs`` folder inside a project root. This folder should contain
   text files with `pip requirements <http://pip.openplans.org/requirement-format.html>`_.

   One file is special: :file:`reqs/all.txt`. This is the main requirements
   file. List all project requirements here one-by-one or (preferrable) by
   including other requirement files using "-r" syntax.


The project should look like that after finishing steps 1-5::

    my_project
        ...
        config_templates <- this folder should be copied from django-fab-deploy
            apache.config
            django_wsgi.py
            hgrc
            nginx.config

        reqs             <- a folder with project's pip requirement files
            all.txt      <- main requirements file, list all requirements in this file
            active.txt   <- put recently modified requirements here
            ...          <- you can provide extra files and include them with '-r' syntax in e.g. all.txt

        fabfile.py       <- your project's Fabric deployment script
        config.py        <- this file should be included in settings.py and ignored in .hgignore
        config.server.py <- this is a production django config template
        settings.py
        manage.py

The project is now ready to be deployed.

Prepare the server
------------------

1. If there is no linux account for ``env.user``
   then add a new linux server user, manually or using

   ::

       fab create_linux_account:"/home/kmike/.ssh/id_rsa.pub"

   You'll need the ssh public key.
   :func:`create_linux_account<fab_deploy.system.create_linux_account>`
   creates a new linux user and uploads provided ssh key. Test that ssh
   login is working::

       ssh example@example.com

   .. note::

       Fabric commands should be executed in shell from the project root
       on local machine (not from the python console, not on server shell).

   SSH keys for other developers can be added at any time::

       fab ssh_add_key:"/home/kmike/coworker-keys/ivan.id_dsa.pub"

2. Setup the database. django-fab-deploy can install mysql and create empty
   DB for the project::

       fab mysql_install
       fab mysql_create_db

   :func:`mysql_install<fab_deploy.mysql.mysql_install>` does
   nothing if mysql is already installed on server. Otherwise it installs
   mysql-server package and sets root password to ``env.conf['DB_PASSWORD']``.

   :func:`mysql_create_db<fab_deploy.mysql.mysql_create_db>` creates a new
   empty database named ``env.conf['INSTANCE_NAME']`` (it equals to
   ``env.user`` by default).

   .. note::

        If non-root mysql user is used then you'd better create DB and
        grant necessary priveleges manually.


3. If you feel brave you can now run ``fab full_deploy`` from the project root
   and get a working django site.

   This command:

   * installs necessary system and python packages
   * configures apache and ngnix
   * creates virtualenv
   * uploads project to the server
   * runs ``python manage.py syncdb`` and ``python manage.py migrate`` commands
     on server

   Project sources will be available under ``~/src/<instance_name>``, virtualenv
   will be placed in ``~/envs/<instance_name>``.

   .. warning::

      django-fab-deploy disables 'default' apache and nginx sites and
      takes over 'ports.conf' so apache is no longer listening to 80 port.

      If there are other sites on server (not managed by django-fab-deploy)
      they may become unaccessible due to these changes.

