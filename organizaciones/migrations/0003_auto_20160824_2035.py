# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '0002_auto_20160822_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinica',
            name='obraSocial',
            field=models.ManyToManyField(to='organizaciones.ObraSocial'),
        ),
    ]
