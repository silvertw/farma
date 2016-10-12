# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0010_auto_20161010_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallefactura',
            name='subtotal',
        ),
        migrations.AddField(
            model_name='piedefactura',
            name='subtotal',
            field=models.DecimalField(default=0, max_digits=8, decimal_places=2),
        ),
    ]
