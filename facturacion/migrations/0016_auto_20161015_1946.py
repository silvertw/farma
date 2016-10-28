# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0015_formadepago_pago'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pago',
            name='fecha',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='importe',
        ),
    ]
