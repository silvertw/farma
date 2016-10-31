# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0016_auto_20161015_1946'),
    ]

    operations = [
        migrations.DeleteModel(
            name='formaDePago',
        ),
        migrations.DeleteModel(
            name='Pago',
        ),
    ]
