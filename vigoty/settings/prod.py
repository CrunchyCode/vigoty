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
CELERY_BROKER_URL = 'amqp://guest@localhost//'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Lima'
# CELERYBEAT_SCHEDULE = {
#     'task-number-one': {
#         'task': 'negocio.tasks.prueba_celery',
#         'schedule': crontab(hour=18, minute=32)
#     },
#     # 'task-number-two': {
#     #     'task': 'app2.tasks.task_number_two',
#     #     'schedule': crontab(minute=0, hour='*/3,10-19')
#     # }
# }
# CELERY_TIMEZONE = 'America/Lima'

# CELERYBEAT_SCHEDULE = {
#     # executes every night at 4:50
#     'every-night': {
#         'task': 'prueba_celery',
#         'schedule': crontab(hour=17, minute=10)
#     }
# }

django.setup()
LOGIN_URL = reverse('login')
LOGIN_REDIRECT_URL = reverse('tienda')
LOGOUT_REDIRECT_URL = reverse('landing')
