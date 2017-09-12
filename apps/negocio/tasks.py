from __future__ import absolute_import, unicode_literals
from celery import task


@task()
def prueba_celery():
    print('Ola k ase: desde CELERY!!')
    return 'ola k ase CELERY!'


# @periodic_task(
#     run_every=(crontab(hour=17, minute=10)),
#     name="segunda_prueba",
#     ignore_result=True
# )
# def segunda_prueba():
#     print('Ola k ase: desde CELERY!!')
