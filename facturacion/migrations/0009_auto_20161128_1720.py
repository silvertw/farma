# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0008_auto_20161128_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piedefacturaaclinica',
            name='factura',
            field=models.OneToOneField(null=True, to='facturacion.FacturaAclinica'),
        ),
        migrations.AlterField(
            model_name='piedefacturadeproveedor',
            name='factura',
            field=models.OneToOneField(null=True, to='facturacion.FacturaDeProveedor'),
        ),
    ]
