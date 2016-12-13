from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from pedidos import config
from pedidos import models as pLabModel
from pedidos.models import PedidoAlaboratorio
from pedidos.models import PedidoDeClinica
from django.db.models import Avg, Max, Min, Sum


class Factura(models.Model):

    TIPO = (
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D")
    )
    tipo = models.PositiveIntegerField(choices=TIPO)
    fecha = models.DateField()
    titular = models.CharField(max_length=45,default="Propietario")
    pagada = models.BooleanField(default=False)

    class Meta:
        abstract = True

class DetalleFactura(models.Model):

    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(config.MAXIMA_CANTIDAD_MEDICAMENTOS)])
    precioUnitario = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    importe = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    class Meta:
        abstract = True

class PieDeFactura(models.Model):
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    class Meta:
        abstract = True


#==================================CONCRETAS============================================================================

#============================================FACTURA DE PROVEEDORES=====================================================
class FacturaDeProveedor(Factura):

    identificador = models.CharField(max_length=45,primary_key=True)
    pedidoRel = models.OneToOneField(PedidoAlaboratorio,null=True)

    def __str__(self):
        return "%s - %s %s" % (self.tipo, self.identificador, self.titular)

    def get_detalles(self):
        response = []
        if self.identificador:
            response = DetalleFacturaDeProveedor.objects.filter(factura=self)
        return response


class DetalleFacturaDeProveedor(DetalleFactura):
    renglon = models.AutoField(primary_key=True)
    medicamento = models.ForeignKey('medicamentos.Medicamento')
    factura = models.ForeignKey('FacturaDeProveedor', null=True, on_delete=models.CASCADE)


class pieDeFacturaDeProveedor(PieDeFactura):
    FILTROS = ["desde", "hasta"]
    FILTERMAPPER = {
        'desde': "factura__fecha__gte",
        'hasta': "factura__fecha__lte",
    }
    factura = models.OneToOneField('FacturaDeProveedor',null=True)

    #Facturas que se pagaron entre dos fechas determinadas.
    #Precondicion las fechas deben tener el formato 'xxxx-xx-xx'.
    def get_facturasPagadas(self,fechaInicial,fechaFinal):
        return pieDeFacturaDeProveedor.objects.filter(
            factura__fecha__range=[fechaInicial,fechaFinal],
            factura__pagada=True)

    def get_cantidad_facturasPagadas(self,fechaInicial,fechaFinal):
        return pieDeFacturaDeProveedor.objects.filter(
            factura__fecha__range=[fechaInicial,fechaFinal],
            factura__pagada=True).count()

    def get_facturasImpagas(self,fechaInicial,fechaFinal):
        return pieDeFacturaDeProveedor.objects.filter(
            factura__fecha__range=[fechaInicial,fechaFinal],
            factura__pagada=False)

    def get_cantidad_facturasImpagas(self,fechaInicial,fechaFinal):
        return pieDeFacturaDeProveedor.objects.filter(
            factura__fecha__range=[fechaInicial,fechaFinal],
            factura__pagada=False).count()

    def get_totalFacturasPagadas(self):
        return pieDeFacturaDeProveedor.objects.filter(factura__pagada=True)

    def get_totalFacturasImpagas(self):
        return pieDeFacturaDeProveedor.objects.filter(factura__pagada=False)

    def get_monto_pagado_entre(self,fechaInicial,fechaFinal):
        resultDic=pieDeFacturaDeProveedor.objects.filter(
            factura__fecha__range=[fechaInicial,fechaFinal],
            factura__pagada=True).aggregate(Sum('total'))
        return resultDic['total__sum']

    def get_monto_a_pagar(self):
        resultDic=pieDeFacturaDeProveedor.objects.filter(factura__pagada=False).aggregate(Sum('total'))
        return resultDic['total__sum']

    #Cuanto se le pago a un proovedor entre dos fechas determinadas
    def get_monto_pagados_aProv_entre(self,proveedor,fechaInicial,fechaFinal):
        resultDic = pieDeFacturaDeProveedor.objects.filter(
                       factura__fecha__range=[fechaInicial,fechaFinal],
                       factura__pagada=True,
                       factura__pedidoRel__laboratorio__razonSocial=proveedor
                    ).aggregate(Sum('total'))
        return resultDic['total__sum']

    #Ranking de montos pagados a proveedores entre dos fechas determinadas.
    def get_rank_montosPagos_aProv_entre(self,fechaInicial,fechaFinal):
         pagadas = pieDeFacturaDeProveedor.objects.filter(
                       factura__fecha__range=[fechaInicial,fechaFinal],
                       factura__pagada=True
                   )
         resumen={}
         for pagada in pagadas:
            proveedor=pagada.factura.pedidoRel.laboratorio.razonSocial
            if not proveedor in resumen:
                resumen[proveedor]=self.monto_pagados_aProv_entre(proveedor,fechaInicial,fechaFinal)

         ranking=resumen.items()
         ranking.sort(key=lambda x: x[1],reverse=True)#Ordenado de mayor a menor segun monto que se le pago
         return ranking

    #Proveedor al que mas se le pago entre dos fechas determinadas
    def get_max_montoPagado_aProv_entre(self,fechaInicial,fechaFinal):
         ranking = self.rank_montosPagos_aProv_entre(fechaInicial,fechaFinal)
         return ranking[0]



#====================================FACTURACION A CLINICA===================================================
class FacturaAclinica(Factura):
    identificador=models.AutoField(primary_key=True)
    pedidoRel = models.OneToOneField(PedidoDeClinica,null=True)

    def __str__(self):
        return "%s - %s %s" % (self.tipo, self.identificador, self.titular)

    def get_detalles(self):
        response = []
        if self.identificador:
            response = DetalleFacturaAclinica.objects.filter(factura=self)
        return response


class DetalleFacturaAclinica(DetalleFactura):
    renglon = models.AutoField(primary_key=True)
    medicamento = models.ForeignKey('medicamentos.Medicamento')
    factura = models.ForeignKey('FacturaAclinica', null=True, on_delete=models.CASCADE)

class pieDeFacturaAclinica(PieDeFactura):
    FILTROS = ["desde", "hasta"]
    FILTERMAPPER = {
        'desde': "factura__fecha__gte",
        'hasta': "factura__fecha__lte",
    }
    factura = models.OneToOneField('FacturaAclinica',null=True)

#==================================================================================================

class formaDePago(models.Model):
    formaPago=models.CharField(max_length=45)
    def __str__(self):
        return self.formaPago

class Pago(models.Model):
    factura = models.ForeignKey('FacturaDeProveedor',null=True)
    importe = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fecha = models.DateField()
    observaciones = models.CharField(max_length=120,null=True)
    formaDePago = models.ForeignKey('formaDePago',null=True)

    def __str__(self):
        return "fecha: %s - importe: %s - obs.: %s - forma de pago: %s" % (self.fecha, self.importe, self.observaciones, self.formaDePago)



