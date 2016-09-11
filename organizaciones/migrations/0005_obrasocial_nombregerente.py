# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '0004_auto_20160824_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='obrasocial',
            name='nombreGerente',
            field=models.CharField(max_length=80, blank=True),
        ),
    ]
