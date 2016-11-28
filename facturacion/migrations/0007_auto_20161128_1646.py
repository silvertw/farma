# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0006_auto_20161128_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piedefacturaaclinica',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='piedefacturadeproveedor',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
