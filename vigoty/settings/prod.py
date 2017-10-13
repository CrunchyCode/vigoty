from __future__ import absolute_import, unicode_literals
from .base import *
from celery.schedules import crontab

DEBUG = False

ALLOWED_HOSTS = ['vigoty.com', '104.236.18.69']

PRODUCTION_APPS = []

INSTALLED_APPS += PRODUCTION_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

# AMAZON S3
AWS_STORAGE_BUCKET_NAME = 'vigoty-do'

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'vigoty.s3.StaticStorage'
STATIC_URL = 'https://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/' + STATICFILES_LOCATION + '/'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'vigoty.s3.MediaStorage'
MEDIA_URL = 'https://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/' + MEDIAFILES_LOCATION + '/'

AWS_QUERYSTRING_AUTH = False

# CELERY SETTINGS
CELERY_USER = os.getenv('RABBITMQ_DEFAULT_USER')
CELERY_PASSWORD = os.getenv('RABBITMQ_DEFAULT_PASS')

CELERY_BROKER_URL = 'amqp://%s:%s@rabbitmq:5672//' % (CELERY_USER, CELERY_PASSWORD)
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
