# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0005_auto_20161127_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturaaclinica',
            name='titular',
            field=models.CharField(default=b'Propietario', max_length=45),
        ),
        migrations.AddField(
            model_name='facturadeproveedor',
            name='titular',
            field=models.CharField(default=b'Propietario', max_length=45),
        ),
    ]
