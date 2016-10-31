# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0014_auto_20161015_0013'),
    ]

    operations = [
        migrations.CreateModel(
            name='formaDePago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('formaPago', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('importe', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('fecha', models.DateField()),
            ],
        ),
    ]
