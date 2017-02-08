# - encode: utf-8 -
from django.db import models
from organizaciones.models import Laboratorio
from organizaciones.models import Farmacia
from django.core.validators import MaxValueValidator, MinValueValidator
from pedidos import config as pconfig
from django.db.models import Q
from django.db.models import Avg, Max, Min, Sum
from . import config
import datetime


class Medicamento(models.Model):
    FILTROS = ["nombreFantasia__nombreF__icontains", 'laboratorio__razonSocial__icontains']
    formulas = models.ManyToManyField('Monodroga',  through='Dosis')
    nombreFantasia = models.ForeignKey('NombreFantasia')
    presentacion = models.ForeignKey('Presentacion')
    codigoBarras = models.CharField("Codigo de barras", max_length=17, unique=True, error_messages={'unique': "Este codigo de barras ya esta cargado"})
    laboratorio = models.ForeignKey(Laboratorio, related_name="medicamentos")
    stockMinimo = models.PositiveIntegerField("Stock minimo de reposicion", validators=[MinValueValidator(1),
                                                                            MaxValueValidator(config.MAXIMO_STOCK_MINIMO)])
    precioDeVenta = models.DecimalField("Precio de venta", max_digits=12, decimal_places=2)

    def __str__(self):
        return "%s %s" % (self.nombreFantasia, self.presentacion)

    def get_stock(self):
        if self.id:
            stockTotal = 0
            lotes = self.get_lotes_activos()
            for lote in lotes:
                stockTotal += lote.stock
            return stockTotal

    def get_lotes_con_stock(self):#Hay procedimientos que exigen que el stock sea mayor a 0.
        lotes = self.get_lotes_activos()
        return lotes.filter(stock__gt=0)

    def get_lotesPverGlobal(self):#Para ver el stock global no interesa que el stock sea mayor a 0.
        lotes = self.get_lotes_activos()
        return lotes

    def tiene_lotes(self):
        if self.get_lotes_activos():
            return True
        else:
            return False

    def get_lotes_activos(self):
        if self.id:
            lim = datetime.date.today() + datetime.timedelta(weeks=pconfig.SEMANAS_LIMITE_VENCIDOS)
            return Lote.objects.filter(medicamento=self, fechaVencimiento__gte=lim)
            #StockDistribuidoEnFarmacias.objects.filter(lote__medicamanto=self,lote__fechaVencimiento__gte=lim)

        return None

class Presentacion(models.Model):
    FILTROS = ["descripcion__icontains"]
    descripcion = models.CharField(max_length=45)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), 
                                                      MaxValueValidator(config.MAXIMA_CANTIDAD_PRESENTACION)])
    unidadMedida = models.CharField("Unidad de medida", max_length=45)

    def __str__(self):
        return "%s - %s %s" % (self.descripcion, self.cantidad, self.unidadMedida)


class Formula(models.Model):
    monodroga = models.ForeignKey('Monodroga')
    dosis = models.ForeignKey('Dosis')


class Monodroga(models.Model):
    FILTROS = ["nombre__icontains"]
    nombre = models.CharField(max_length=75, unique=True, error_messages={'unique': "Esta monodroga ya esta cargada"})

    def __str__(self):
        return "%s" % self.nombre


class Dosis(models.Model):
    UNIDADES = (
        (1, "ml"),
        (2, "mg")
    )
    medicamento = models.ForeignKey(Medicamento)
    monodroga = models.ForeignKey(Monodroga)
    unidad = models.PositiveIntegerField(choices=UNIDADES)
    cantidad = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1), 
                                                     MaxValueValidator(config.MAXIMA_CANTIDAD_DOSIS)])

    def __str__(self):
        return "%s - %s" % (self.cantidad, self.get_unidad_display())


class NombreFantasia(models.Model):
    FILTROS = ["nombreF__icontains"]
    nombreF = models.CharField(max_length=75,  unique=True,error_messages={'unique': "Este nombre de fantasia ya esta cargado"})

    def __str__(self):
        return "%s" % self.nombreF


class Lote(models.Model):
    FILTROS = ["numero__icontains"]
    numero = models.PositiveIntegerField(unique=True, error_messages={'unique': "Este numero de lote ya esta cargado"})
    fechaVencimiento= models.DateField()
    stock = models.PositiveIntegerField()#Stock que hay en drogueria de este lote.
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    medicamento = models.ForeignKey('Medicamento', on_delete=models.CASCADE)
    stockFarmaYfarmacias = models.ForeignKey('StockFarmayFarmacias',null=True)

    def __str__(self):
        return "%s" % (self.numero)

    def to_json(self):
        if self.numero:
            return {
                'nroLote': self.numero,
                'fechaVencimiento': self.fechaVencimiento.strftime("%d/%m/%y"),
                'stock': self.stock
            }

    def get_lote_nro(self,nroLote):
        return Lote.objects.get(numero = nroLote)

    #===============IMPORTANTE-DIEGO-FORMA CORRECTA-LOGICA DE NEGOCIO===========================
    #def enviarAFarmacia(self, farmacia, cantidad):
    #    if self.stock < cantidad:
    #        raise "No puedo descontar %d" % cantidad
    #    self.stock -= cantidad
    #    st = StockDistribuidoEnFarmacias(lote=self, cantidad=cantidad, farmacia=farmacia)
    #    st.save()
    #    self.stock_en_farmacias.add(st)
    #    self.save()
    #    return st

class StockFarmayFarmacias(models.Model):
    stockFarma=models.PositiveIntegerField(default=0)#Stock que hay en farma de un determinado lote.
    stockFarmacias=models.PositiveIntegerField(default=0)#Stock que hay en farmacias distribuido de un lote determinado.

    def __str__(self):
        return "Stock total en drogueria: %s" % (self.stockFarma)


class StockDistribuidoEnFarmacias(models.Model):

    FILTROS = ["farmacia", "numLote", "medicamento"]
    FILTERMAPPER = {
        'farmacia': "farmacia__razonSocial__icontains",
        'numLote': "lote__numero__icontains",
        'medicamento': "lote__medicamento__nombreFantasia__nombreF__icontains",

    }
    lote=models.ForeignKey(Lote, null=True)
    cantidad=models.PositiveIntegerField(default=0)
    farmacia=models.ForeignKey(Farmacia,null=True)

    def miNombreFantasia(self):
        return self.lote.medicamento.nombreFantasia.nombreF

    #Devuelve un stock dist en base a la razon social y al numero de lote
    def get_dist_farmaciaRs_y_loteNro(self,farmaciaRs,nroLote):
        stockDist = StockDistribuidoEnFarmacias.objects.get(farmacia__razonSocial=farmaciaRs,lote__numero=nroLote)
        return stockDist

    def get_exist_farmaciaRs_y_loteNro(self,farmacia,lote):
        return StockDistribuidoEnFarmacias.objects.filter(farmacia__razonSocial=farmacia,lote__numero=lote).exists()

    def __str__(self):
        return "nro. lote:%s - Cantidad en: %s - %s" % (self.lote, self.farmacia, self.cantidad)


