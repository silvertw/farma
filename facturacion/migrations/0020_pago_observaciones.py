# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0019_auto_20161016_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='observaciones',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
