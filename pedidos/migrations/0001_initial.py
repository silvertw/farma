# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '__first__'),
        ('organizaciones', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='detalleDeMovimientos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('farmacia', models.CharField(max_length=50)),
                ('lote', models.PositiveIntegerField()),
                ('cantidadQuitada', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedidoAlaboratorio',
            fields=[
                ('renglon', models.AutoField(serialize=False, primary_key=True)),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
                ('cantidadPendiente', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedidoDeClinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
                ('cantidadPendiente', models.PositiveIntegerField(default=0)),
                ('estaPedido', models.BooleanField(default=False)),
                ('medicamento', models.ForeignKey(to='medicamentos.Medicamento')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Detalles de Pedidos de Clinica',
            },
        ),
        migrations.CreateModel(
            name='DetallePedidoDeFarmacia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2147483647)])),
                ('cantidadPendiente', models.PositiveIntegerField(default=0)),
                ('estaPedido', models.BooleanField(default=False)),
                ('medicamento', models.ForeignKey(to='medicamentos.Medicamento')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Detalles de Pedidos de Farmacia',
            },
        ),
        migrations.CreateModel(
            name='DetalleRemitoDeClinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('detallePedidoDeClinica', models.ForeignKey(to='pedidos.DetallePedidoDeClinica')),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRemitoDeFarmacia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('detallePedidoDeFarmacia', models.ForeignKey(to='pedidos.DetallePedidoDeFarmacia')),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRemitoLaboratorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('detallePedidoLaboratorio', models.ForeignKey(to='pedidos.DetallePedidoAlaboratorio')),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRemitoMedicamentosVencido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('dependencia', models.CharField(max_length=50)),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
                ('medicamento', models.ForeignKey(to='medicamentos.Medicamento')),
            ],
        ),
        migrations.CreateModel(
            name='movimientosDeStockDistribuido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('movimiento', models.TextField()),
                ('farmaciaDeDestino', models.CharField(max_length=50)),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoAlaboratorio',
            fields=[
                ('nroPedido', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('estado', models.CharField(default=b'Pendiente', max_length=25, blank=True)),
                ('facturaAsociada', models.BooleanField(default=False)),
                ('laboratorio', models.ForeignKey(to='organizaciones.Laboratorio')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoDeClinica',
            fields=[
                ('nroPedido', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('medicoAuditor', models.CharField(max_length=80)),
                ('facturaAsociada', models.BooleanField(default=False)),
                ('clinica', models.ForeignKey(to='organizaciones.Clinica')),
                ('obraSocial', models.ForeignKey(to='organizaciones.ObraSocial')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Pedidos de Clinica',
            },
        ),
        migrations.CreateModel(
            name='PedidoDeFarmacia',
            fields=[
                ('nroPedido', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('estado', models.CharField(max_length=25, blank=True)),
                ('tieneMovimientos', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Pedidos de Farmacia',
                'permissions': (('generar_reporte_farmacia', 'Puede generar el reporte de pedidos a farmacia'),),
            },
        ),
        migrations.CreateModel(
            name='RemitoDeClinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('pedidoDeClinica', models.ForeignKey(to='pedidos.PedidoDeClinica')),
            ],
        ),
        migrations.CreateModel(
            name='RemitoDeFarmacia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='RemitoLaboratorio',
            fields=[
                ('nroRemito', models.BigIntegerField(unique=True, serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('laboratorio', models.ForeignKey(to='organizaciones.Laboratorio')),
                ('pedidoLaboratorio', models.ForeignKey(to='pedidos.PedidoAlaboratorio')),
            ],
        ),
        migrations.CreateModel(
            name='RemitoMedicamentosVencidos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.BigIntegerField()),
                ('fecha', models.DateField()),
                ('laboratorio', models.ForeignKey(to='organizaciones.Laboratorio')),
            ],
        ),
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
        migrations.AddField(
            model_name='remitodefarmacia',
            name='pedidoFarmacia',
            field=models.ForeignKey(to='pedidos.PedidoDeFarmacia'),
        ),
        migrations.AddField(
            model_name='pedidodefarmacia',
            name='farmacia',
            field=models.ForeignKey(to='organizaciones.Farmacia'),
        ),
        migrations.AddField(
            model_name='pedidoalaboratorio',
            name='remitoVencidosAsociado',
            field=models.OneToOneField(null=True, blank=True, to='pedidos.RemitoMedicamentosVencidos'),
        ),
        migrations.AddField(
            model_name='movimientosdestockdistribuido',
            name='pedidoMov',
            field=models.ForeignKey(to='pedidos.PedidoDeFarmacia'),
        ),
        migrations.AddField(
            model_name='detalleremitomedicamentosvencido',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoMedicamentosVencidos'),
        ),
        migrations.AddField(
            model_name='detalleremitolaboratorio',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoLaboratorio'),
        ),
        migrations.AddField(
            model_name='detalleremitodefarmacia',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoDeFarmacia'),
        ),
        migrations.AddField(
            model_name='detalleremitodeclinica',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoDeClinica'),
        ),
        migrations.AddField(
            model_name='detallepedidodefarmacia',
            name='pedidoDeFarmacia',
            field=models.ForeignKey(to='pedidos.PedidoDeFarmacia'),
        ),
        migrations.AddField(
            model_name='detallepedidodeclinica',
            name='pedidoDeClinica',
            field=models.ForeignKey(to='pedidos.PedidoDeClinica'),
        ),
        migrations.AddField(
            model_name='detallepedidoalaboratorio',
            name='detallePedidoFarmacia',
            field=models.ForeignKey(blank=True, to='pedidos.DetallePedidoDeFarmacia', null=True),
        ),
        migrations.AddField(
            model_name='detallepedidoalaboratorio',
            name='medicamento',
            field=models.ForeignKey(to='medicamentos.Medicamento'),
        ),
        migrations.AddField(
            model_name='detallepedidoalaboratorio',
            name='pedido',
            field=models.ForeignKey(to='pedidos.PedidoAlaboratorio', null=True),
        ),
        migrations.AddField(
            model_name='detalledemovimientos',
            name='movimiento',
            field=models.ForeignKey(to='pedidos.movimientosDeStockDistribuido', null=True),
        ),
    ]
