# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturaaclinica',
            name='identificador',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='facturaaclinica',
            name='tipo',
            field=models.PositiveIntegerField(default=1, choices=[(1, b'A'), (2, b'B'), (3, b'C'), (4, b'D')]),
        ),
        migrations.AlterField(
            model_name='facturaaclinica',
            name='titular',
            field=models.CharField(default=b'Propietario', max_length=45),
        ),
    ]
