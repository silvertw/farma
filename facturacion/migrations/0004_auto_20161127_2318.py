# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0003_auto_20161127_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='pieDeFacturaDeProveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subtotal', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('iva', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('total', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('factura', models.OneToOneField(null=True, to='facturacion.FacturaDeProveedor')),
            ],
        ),
        migrations.RemoveField(
            model_name='piedefactura',
            name='factura',
        ),
        migrations.DeleteModel(
            name='pieDeFactura',
        ),
    ]
