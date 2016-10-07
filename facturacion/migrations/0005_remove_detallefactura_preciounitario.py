# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0004_detallefactura_preciounitario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallefactura',
            name='precioUnitario',
        ),
    ]
