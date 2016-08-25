# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '0003_auto_20160824_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinica',
            name='obraSocial',
            field=models.ManyToManyField(to='organizaciones.ObraSocial', blank=True),
        ),
    ]
