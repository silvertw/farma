# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0005_remove_detallefactura_preciounitario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='fecha',
            field=models.DateField(),
        ),
    ]
