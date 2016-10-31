# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0007_factura_iva'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallefactura',
            name='importe',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=2),
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='precioUnitario',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=2),
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='subtotal',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=2),
        ),
    ]
