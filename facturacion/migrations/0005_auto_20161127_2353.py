# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0004_auto_20161127_2318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facturaaclinica',
            name='titular',
        ),
        migrations.RemoveField(
            model_name='facturadeproveedor',
            name='titular',
        ),
        migrations.AlterField(
            model_name='facturaaclinica',
            name='identificador',
            field=models.CharField(max_length=45, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='facturaaclinica',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(1, b'A'), (2, b'B'), (3, b'C'), (4, b'D')]),
        ),
    ]
