# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-01 17:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('negocio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=6)),
                ('total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('fecha_realizado', models.DateField(auto_now=True)),
                ('estado', models.CharField(default='1', max_length=1)),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='negocio.Menu')),
            ],
        ),
    ]