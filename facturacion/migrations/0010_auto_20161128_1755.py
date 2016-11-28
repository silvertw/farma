# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0009_auto_20161128_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturaaclinica',
            name='identificador',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
