# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0022_pago_factura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='factura',
            field=models.ForeignKey(to='facturacion.Factura', null=True),
        ),
    ]
