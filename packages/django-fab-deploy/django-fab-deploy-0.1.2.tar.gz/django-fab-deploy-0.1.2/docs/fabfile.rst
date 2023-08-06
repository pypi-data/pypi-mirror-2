fabfile.py API
==============

fabfile.py long example
-----------------------

::

    from fabric.api import *
    from fab_deploy import *

    def stage():

        # how to connect via ssh:
        env.hosts = ['my-stage-server.com']   # host
        env.user = 'user'                     # user (must not be root)

        # instance parameters
        env.conf = dict(

            # distinct instance name
            INSTANCE_NAME = "my_site",

            # server name. It will be used for web server configs.
            SERVER_NAME = "my-site.example.com",

            # DB credentials
            DB_NAME = 'my_site_testing',
            DB_PASSWORD = '123',

            # apache and mod_wsgi config
            PROCESSES = 1,
            THREADS = 5,

            # port should be distinct from other instances' ports
            APACHE_PORT = 8083,

            # named hg branch that will be active by default
            HG_BRANCH = 'default',

            # any other parameters. They will be available in config
            # templates as template variables
            VERSION = 'STAGING',
        )
        update_env()

    def prod():
        env.hosts = ['my-site.com']
        env.user = 'user'
        env.conf = dict(

            # this should be different if stage and production
            # instances share the same server
            INSTANCE_NAME = "my_site",

            SERVER_NAME = "my-site.com",

            # DB credentials
            DB_NAME = 'my_site_production',
            DB_PASSWORD = '345',

            # apache and mod_wsgi config
            PROCESSES = 5,
            THREADS = 15,

            # port should be distinct from other instances'
            # ports on the same server
            APACHE_PORT = 8083,

            # named hg branch that will be active by default
            HG_BRANCH = 'production',

            # any other parameters. They will be available in config
            # templates as template variables
            VERSION = 'PROD',
        )
        update_env()

    stage() # use stage versions as default
