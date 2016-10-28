# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0018_formadepago_pago'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pago',
            name='formaDePago',
        ),
        migrations.AddField(
            model_name='pago',
            name='formaDePago',
            field=models.ForeignKey(to='facturacion.formaDePago', null=True),
        ),
    ]
