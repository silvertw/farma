# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '__first__'),
        ('facturacion', '0002_auto_20161118_0753'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleFacturaDeProveedor',
            fields=[
                ('renglon', models.AutoField(serialize=False, primary_key=True)),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
                ('precioUnitario', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('importe', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('factura', models.ForeignKey(to='facturacion.FacturaDeProveedor', null=True)),
                ('medicamento', models.ForeignKey(to='medicamentos.Medicamento')),
            ],
        ),
        migrations.RemoveField(
            model_name='detallefactura',
            name='factura',
        ),
        migrations.RemoveField(
            model_name='detallefactura',
            name='medicamento',
        ),
        migrations.DeleteModel(
            name='DetalleFactura',
        ),
    ]
