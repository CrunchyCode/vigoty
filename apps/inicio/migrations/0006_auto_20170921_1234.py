# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-21 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0005_auto_20170921_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccion',
            name='lat',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
        migrations.AlterField(
            model_name='direccion',
            name='lng',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
    ]
