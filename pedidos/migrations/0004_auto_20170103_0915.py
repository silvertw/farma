# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_auto_20181125_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoFarmaciaMobile',
            fields=[
                ('pedidodefarmacia_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pedidos.PedidoDeFarmacia')),
                ('pedidoCerrado', models.BooleanField(default=False)),
                ('notificado', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('pedidos.pedidodefarmacia',),
        ),
        migrations.RemoveField(
            model_name='pedidodefarmacia',
            name='mobile',
        ),
    ]
