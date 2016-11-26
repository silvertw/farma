# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='farmacia',
            field=models.ForeignKey(blank=True, to='organizaciones.Farmacia', null=True),
        ),
    ]
