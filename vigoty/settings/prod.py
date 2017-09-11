from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

PRODUCTION_APPS = []

INSTALLED_APPS += PRODUCTION_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# AMAZON S3
AWS_STORAGE_BUCKET_NAME = 'vigoty-do'

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'vigoty.s3.StaticStorage'
STATIC_URL = 'https://'+AWS_STORAGE_BUCKET_NAME+'.s3.amazonaws.com/'+STATICFILES_LOCATION+'/'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'vigoty.s3.MediaStorage'
MEDIA_URL = 'https://'+AWS_STORAGE_BUCKET_NAME+'.s3.amazonaws.com/'+MEDIAFILES_LOCATION+'/'

AWS_QUERYSTRING_AUTH = False

django.setup()
LOGIN_URL = reverse('login')
LOGIN_REDIRECT_URL = reverse('tienda')
LOGOUT_REDIRECT_URL = reverse('landing')
