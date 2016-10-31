# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '__first__'),
        ('facturacion', '0012_auto_20161012_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='pedidos',
            field=models.OneToOneField(null=True, to='pedidos.PedidoAlaboratorio'),
        ),
    ]
