# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0021_factura_pagada'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='factura',
            field=models.OneToOneField(null=True, to='facturacion.Factura'),
        ),
    ]
