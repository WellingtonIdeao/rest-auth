from .base import *
import environ

environ.Env.read_env()
env = environ.Env(
    DEBUG=(bool, True)
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # read os.environ['SQLITE_URL']
    'default': env.db_url('SQLITE_URL'),
}

# add  a custom name for test database
DATABASES['default'].update({'TEST': {'NAME': 'test_rest_auth_db'}})


