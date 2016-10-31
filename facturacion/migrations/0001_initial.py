# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('renglon', models.AutoField(serialize=False, primary_key=True)),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('tipo', models.PositiveIntegerField(choices=[(1, b'A'), (2, b'B'), (3, b'C'), (4, b'D')])),
                ('identificador', models.CharField(max_length=45, serialize=False, primary_key=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('titular', models.CharField(max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='factura',
            field=models.ForeignKey(to='facturacion.Factura', null=True),
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='medicamento',
            field=models.ForeignKey(to='medicamentos.Medicamento'),
        ),
    ]
