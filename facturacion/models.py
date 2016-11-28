from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from pedidos import config
from pedidos import models as pLabModel
from pedidos.models import PedidoAlaboratorio
from pedidos.models import PedidoDeClinica


class FacturaDeProveedor(models.Model):

    TIPO = (
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D")
    )
    identificador = models.CharField(max_length=45,primary_key=True)
    tipo = models.PositiveIntegerField(choices=TIPO)
    fecha = models.DateField()
    titular = models.CharField(max_length=45,default="Propietario")
    pagada = models.BooleanField(default=False)
    pedidoRel = models.OneToOneField(PedidoAlaboratorio,null=True)

    def __str__(self):
        return "%s - %s %s" % (self.tipo, self.identificador, self.titular)

    def get_detalles(self):
        response = []
        if self.identificador:
            response = DetalleFacturaDeProveedor.objects.filter(factura=self)
        return response


class DetalleFacturaDeProveedor(models.Model):
    renglon = models.AutoField(primary_key=True)
    medicamento = models.ForeignKey('medicamentos.Medicamento')
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(config.MAXIMA_CANTIDAD_MEDICAMENTOS)])
    precioUnitario = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    importe = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    factura = models.ForeignKey('FacturaDeProveedor', null=True, on_delete=models.CASCADE)


class pieDeFacturaDeProveedor(models.Model):
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    factura = models.OneToOneField('FacturaDeProveedor',null=True)



#====================================FACTURACION A CLINICA===================================================

class FacturaAclinica(models.Model):
    TIPO = (
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D")
    )
    identificador=models.AutoField(primary_key=True)
    tipo = models.PositiveIntegerField(choices=TIPO)
    fecha = models.DateField()
    titular = models.CharField(max_length=45,default="Propietario")
    pagada = models.BooleanField(default=False)
    pedidoRel = models.OneToOneField(PedidoDeClinica,null=True)

    def __str__(self):
        return "%s - %s %s" % (self.tipo, self.identificador, self.titular)

    def get_detalles(self):
        response = []
        if self.identificador:
            response = DetalleFacturaAclinica.objects.filter(factura=self)
        return response


class DetalleFacturaAclinica(models.Model):
    renglon = models.AutoField(primary_key=True)
    medicamento = models.ForeignKey('medicamentos.Medicamento')
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(config.MAXIMA_CANTIDAD_MEDICAMENTOS)])
    precioUnitario = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    importe = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    factura = models.ForeignKey('FacturaAclinica', null=True, on_delete=models.CASCADE)

class pieDeFacturaAclinica(models.Model):
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
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



