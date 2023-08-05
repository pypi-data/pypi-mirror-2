from functools import wraps
from fabric.contrib.files import upload_template
from fabric.api import env

def run_as(user):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            old_user = env.user
            env.user = user
            result = func(*args, **kwargs)
            env.user = old_user
            return result
        return inner
    return decorator

def upload_hosting_template(name, to):
    upload_template('./hosting/templates/'+name, to, env.conf, True)

def update_env():
    HOME_DIR = '/home/%s' % env.user
    ENV_BASE, SRC_BASE = 'envs', 'src'

    if 'INSTANCE_NAME' not in env.conf:
        env.conf['INSTANCE_NAME'] = env.user

    if 'SERVER_NAME' not in env.conf:
        env.conf['SERVER_NAME'] = env.hosts[0]

    defaults = dict(
        HG_BRANCH = 'default',
        DB_NAME = env.conf['INSTANCE_NAME'],
        PROCESSES = 1,
        THREADS = 5,
        HOME_DIR = HOME_DIR,
        ENV_BASE = ENV_BASE,
        SRC_BASE = SRC_BASE,
        ENV_DIR = HOME_DIR + '/' + ENV_BASE + '/' + env.conf['INSTANCE_NAME'],
        SRC_DIR = HOME_DIR + '/' + SRC_BASE + '/' + env.conf['INSTANCE_NAME'],
    )
    defaults.update(env.conf)
    env.conf = defaults
