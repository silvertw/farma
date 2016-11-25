# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_pedidoalaboratorio_remitovencidosasociado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleremitomedicamentosvencido',
            name='dependencia',
            field=models.CharField(max_length=50),
        ),
    ]
