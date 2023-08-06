Custom project layouts
======================

:doc:`guide` describes standard project layout::

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

django-fab-deploy does not enforce this layout. Requirements handling,
config templates placement, local settings file names and project source
folder can be customized using these options:

* :attr:`env.conf.PROJECT_PATH`
* :attr:`env.conf.LOCAL_CONFIG`
* :attr:`env.conf.REMOTE_CONFIG_TEMPLATE`
* :attr:`env.conf.CONFIG_TEMPLATES_PATHS`
* :attr:`env.conf.PIP_REQUIREMENTS_PATH`
* :attr:`env.conf.PIP_REQUIREMENTS`
* :attr:`env.conf.PIP_REQUIREMENTS_ACTIVE`

Example
-------

Let's configure django-fab-deploy to use the following layout::

    my_project
        hosting                 <- a folder with server configs
            staging             <- custom configs for 'staging' server
                apache.config   <- custom apache config for staging server

            production          <- custom configs for 'production' server
                apache.config
                nginx.config

            apache.config       <- default configs
            django_wsgi.py
            nginx.config

        src                     <- django project source files
            apps
                ...

            local_settings.py   <- local settings
            stage_settings.py   <- local settings for staging server
            prod_settings.py    <- local settings for production server

            settings.py
            manage.py

        requirements.txt        <- single file with all pip requirements
        fabfile.py              <- project's Fabric deployment script

It uses subfolder for storing django project sources, single pip requirements
file and different config templates for different servers in
non-default locations.

fabfile.py::

    from fab_deploy import *

    # common layout options
    COMMON_OPTIONS = dict(
        PROJECT_PATH = 'src',
        LOCAL_CONFIG = 'local_settings.py',
        PIP_REQUIREMENTS = 'requirements.txt',
        PIP_REQUIREMENTS_ACTIVE = 'requirements.txt',
        PIP_REQUIREMENTS_PATH = '',
    )

    def staging():
        env.hosts = ['user@staging.example.com']
        env.conf = COMMON_OPTIONS.copy()
        env.conf.update(
            REMOTE_CONFIG_TEMPLATE = 'stage_settings.py',
            CONFIG_TEMPLATES_PATHS = ['hosting/staging', 'hosting'],
        )
        update_env()

    def production():
        env.hosts = ['user@example.com']
        env.conf = COMMON_OPTIONS.copy()
        env.conf.update(
            REMOTE_CONFIG_TEMPLATE = 'prod_settings.py',
            CONFIG_TEMPLATES_PATHS = ['hosting/production', 'hosting'],
        )
        update_env()

