from __future__ import absolute_import, unicode_literals
from celery import task
from datetime import datetime, timedelta
from .models import Menu


@task(name='actualizar_estado_menu')
def actualizar_estado_menu():
    mañana = datetime.now() + timedelta(days=1)
    mañana = mañana.date()
    menus_activos = Menu.objects.filter(disponible='1', estado='2')

    for menu in menus_activos:
        if mañana > menu.fecha_disponibilidad:
            menu.disponible = '2'   # NO DISPONIBLE
            menu.save()


@task(name='tarea_prueba')
def tarea_prueba():
    print('LA TAREA DE PRUEBA')
