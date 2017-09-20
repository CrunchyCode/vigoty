# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-20 16:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inicio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=140)),
                ('referencia', models.TextField()),
                ('street_number', models.CharField(blank=True, max_length=6, null=True)),
                ('route', models.CharField(blank=True, max_length=45, null=True)),
                ('locality', models.CharField(blank=True, max_length=45, null=True)),
                ('administrative_area_level_2', models.CharField(blank=True, max_length=45, null=True)),
                ('administrative_area_level_1', models.CharField(blank=True, max_length=45, null=True)),
                ('country', models.CharField(blank=True, max_length=45, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=15, null=True)),
                ('latitude', models.CharField(max_length=15)),
                ('longitude', models.CharField(max_length=15)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='direccion',
        ),
    ]
