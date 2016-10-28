# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0020_pago_observaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='pagada',
            field=models.BooleanField(default=False),
        ),
    ]
