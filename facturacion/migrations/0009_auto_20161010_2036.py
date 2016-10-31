# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0008_auto_20161010_2016'),
    ]

    operations = [
        migrations.CreateModel(
            name='pieDeFactura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iva', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='detallefactura',
            name='importe',
        ),
        migrations.RemoveField(
            model_name='detallefactura',
            name='precioUnitario',
        ),
        migrations.RemoveField(
            model_name='detallefactura',
            name='subtotal',
        ),
        migrations.RemoveField(
            model_name='factura',
            name='iva',
        ),
        migrations.AddField(
            model_name='piedefactura',
            name='factura',
            field=models.ForeignKey(to='facturacion.Factura', null=True),
        ),
    ]
