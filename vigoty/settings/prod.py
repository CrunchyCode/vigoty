from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

PRODUCTION_APPS = []

INSTALLED_APPS += PRODUCTION_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}
