from __future__ import absolute_import, unicode_literals
from .base import *
from celery.schedules import crontab

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

# CELERY SETTINGS
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Lima'
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULE = {
    'tarea-de-prueba': {
        'task': 'tarea_prueba',
        'schedule': crontab(minute=25)
    },
    'actualizar-estado-menu': {
        'task': 'actualizar_estado_menu',
        'schedule': crontab(hour=23)
    },
}

django.setup()
LOGIN_URL = reverse('login')
LOGIN_REDIRECT_URL = reverse('tienda')
LOGOUT_REDIRECT_URL = reverse('landing')
