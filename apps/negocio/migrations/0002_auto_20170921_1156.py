# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-21 16:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0004_auto_20170921_1156'),
        ('negocio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='administrative_area_level_1',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='administrative_area_level_2',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='country',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='direccion_texto',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='lng',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='locality',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='route',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='street_number',
        ),
        migrations.AddField(
            model_name='menu',
            name='direccion',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='inicio.Direccion'),
            preserve_default=False,
        ),
    ]