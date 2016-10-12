# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0006_auto_20161008_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='iva',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=2),
        ),
    ]
