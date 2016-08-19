# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razonSocial', models.CharField(unique=True, max_length=50)),
                ('cuit', models.CharField(unique=True, max_length=80, error_messages={b'unique': b'Ya existe una organizacion con este CUIT'})),
                ('localidad', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50, blank=True)),
                ('telefono', models.CharField(max_length=80, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Farmacia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razonSocial', models.CharField(unique=True, max_length=50)),
                ('cuit', models.CharField(unique=True, max_length=80, error_messages={b'unique': b'Ya existe una organizacion con este CUIT'})),
                ('localidad', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50, blank=True)),
                ('telefono', models.CharField(max_length=80, blank=True)),
                ('nombreEncargado', models.CharField(max_length=80, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razonSocial', models.CharField(unique=True, max_length=50)),
                ('cuit', models.CharField(unique=True, max_length=80, error_messages={b'unique': b'Ya existe una organizacion con este CUIT'})),
                ('localidad', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50, blank=True)),
                ('telefono', models.CharField(max_length=80, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObraSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razonSocial', models.CharField(unique=True, max_length=50)),
                ('cuit', models.CharField(unique=True, max_length=80, error_messages={b'unique': b'Ya existe una organizacion con este CUIT'})),
                ('localidad', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50, blank=True)),
                ('telefono', models.CharField(max_length=80, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='clinica',
            name='obraSocial',
            field=models.ManyToManyField(to='organizaciones.ObraSocial'),
        ),
    ]
