# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0013_factura_pedidos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='factura',
            old_name='pedidos',
            new_name='pedidoRel',
        ),
    ]
