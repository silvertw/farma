# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0007_auto_20161128_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piedefacturaaclinica',
            name='factura',
            field=models.ForeignKey(to='facturacion.FacturaAclinica', null=True),
        ),
        migrations.AlterField(
            model_name='piedefacturaaclinica',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='piedefacturadeproveedor',
            name='factura',
            field=models.ForeignKey(to='facturacion.FacturaDeProveedor', null=True),
        ),
        migrations.AlterField(
            model_name='piedefacturadeproveedor',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
    ]
