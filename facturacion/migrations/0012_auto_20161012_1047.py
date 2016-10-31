# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0011_auto_20161010_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piedefactura',
            name='factura',
            field=models.OneToOneField(null=True, to='facturacion.Factura'),
        ),
    ]
