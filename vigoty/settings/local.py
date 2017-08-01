from .base import *

DEBUG = True

ALLOWED_HOSTS = []

LOCAL_APPS = []

INSTALLED_APPS += LOCAL_APPS

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

STATIC_URL = '/static/'
STATIC_ROOT = '/static'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
