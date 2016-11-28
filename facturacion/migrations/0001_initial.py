# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '__first__'),
        ('medicamentos', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('renglon', models.AutoField(serialize=False, primary_key=True)),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
                ('precioUnitario', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('importe', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleFacturaAclinica',
            fields=[
                ('renglon', models.AutoField(serialize=False, primary_key=True)),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
                ('precioUnitario', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('importe', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='FacturaDeProveedor',
            fields=[
                ('tipo', models.PositiveIntegerField(choices=[(1, b'A'), (2, b'B'), (3, b'C'), (4, b'D')])),
                ('identificador', models.CharField(max_length=45, serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('titular', models.CharField(max_length=45)),
                ('pagada', models.BooleanField(default=False)),
                ('pedidoRel', models.OneToOneField(null=True, to='pedidos.PedidoAlaboratorio')),
            ],
        ),
        migrations.CreateModel(
            name='FacturaAclinica',
            fields=[
                ('tipo', models.PositiveIntegerField(choices=[(1, b'A'), (2, b'B'), (3, b'C'), (4, b'D')])),
                ('identificador', models.CharField(max_length=45, serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('titular', models.CharField(max_length=45)),
                ('pagada', models.BooleanField(default=False)),
                ('pedidoRel', models.OneToOneField(null=True, to='pedidos.PedidoDeClinica')),
            ],
        ),
        migrations.CreateModel(
            name='formaDePago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('formaPago', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('importe', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('fecha', models.DateField()),
                ('observaciones', models.CharField(max_length=120, null=True)),
                ('factura', models.ForeignKey(to='facturacion.FacturaDeProveedor', null=True)),
                ('formaDePago', models.ForeignKey(to='facturacion.formaDePago', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='pieDeFactura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subtotal', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('iva', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('total', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('factura', models.OneToOneField(null=True, to='facturacion.FacturaDeProveedor')),
            ],
        ),
        migrations.CreateModel(
            name='pieDeFacturaAclinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subtotal', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('iva', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('total', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('factura', models.OneToOneField(null=True, to='facturacion.FacturaAclinica')),
            ],
        ),
        migrations.AddField(
            model_name='detallefacturaaclinica',
            name='factura',
            field=models.ForeignKey(to='facturacion.FacturaAclinica', null=True),
        ),
        migrations.AddField(
            model_name='detallefacturaaclinica',
            name='medicamento',
            field=models.ForeignKey(to='medicamentos.Medicamento'),
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='factura',
            field=models.ForeignKey(to='facturacion.FacturaDeProveedor', null=True),
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='medicamento',
            field=models.ForeignKey(to='medicamentos.Medicamento'),
        ),
    ]
