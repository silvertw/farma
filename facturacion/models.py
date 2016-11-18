from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from pedidos import config
from pedidos import models as pLabModel
from pedidos.models import PedidoAlaboratorio
from pedidos.models import PedidoDeClinica


class Factura(models.Model):

    FILTROS = ["identificador"]
    FILTERMAPPER = {
        'identificador': "identificador__icontains",
    }

    TIPO = (
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D")
    )

    tipo = models.PositiveIntegerField(choices=TIPO)
    identificador = models.CharField(max_length=45,primary_key=True)
    fecha = models.DateField()
    titular = models.CharField(max_length=45)
    pedidoRel = models.OneToOneField(PedidoAlaboratorio,null=True)
    pagada = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s %s" % (self.tipo, self.identificador, self.titular)

    def get_detalles(self):
        response = []
        if self.identificador:
            response = DetalleFactura.objects.filter(Factura=self)
        return response


class DetalleFactura(models.Model):

    factura = models.ForeignKey('Factura', null=True, on_delete=models.CASCADE)
    renglon = models.AutoField(primary_key=True)
    medicamento = models.ForeignKey('medicamentos.Medicamento')
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(config.MAXIMA_CANTIDAD_MEDICAMENTOS)])

    precioUnitario = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    importe = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class pieDeFactura(models.Model):
    factura = models.OneToOneField('Factura',null=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    #@property #Decorador que asigna signo pesos frente al precio unitario
    #def total(self):
    #    return "$%s" % self.total

class formaDePago(models.Model):
    formaPago=models.CharField(max_length=45)
    def __str__(self):
        return self.formaPago

class Pago(models.Model):
    factura = models.ForeignKey('Factura',null=True)
    importe = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fecha = models.DateField()
    observaciones = models.CharField(max_length=120,null=True)
    formaDePago = models.ForeignKey('formaDePago',null=True)

    def __str__(self):
        return "fecha: %s - importe: %s - obs.: %s - forma de pago: %s" % (self.fecha, self.importe, self.observaciones, self.formaDePago)


#====================================FACTURACION A CLINICA===================================================

class FacturaAclinica(models.Model):

    FILTROS = ["identificador"]
    FILTERMAPPER = {
        'identificador': "identificador__icontains",
    }

    TIPO = (
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D")
    )

    tipo = models.PositiveIntegerField(choices=TIPO,default=1)
    identificador=models.AutoField(primary_key=True)
    fecha = models.DateField()
    titular = models.CharField(max_length=45,default="Propietario")
    pedidoRel = models.OneToOneField(PedidoDeClinica,null=True)
    pagada = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s %s" % (self.tipo, self.identificador, self.titular)

    def get_detalles(self):
        response = []
        if self.identificador:
            response = DetalleFactura.objects.filter(Factura=self)
        return response


class DetalleFacturaAclinica(models.Model):

    factura = models.ForeignKey('FacturaAclinica', null=True, on_delete=models.CASCADE)
    renglon = models.AutoField(primary_key=True)
    medicamento = models.ForeignKey('medicamentos.Medicamento')
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(config.MAXIMA_CANTIDAD_MEDICAMENTOS)])

    precioUnitario = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    importe = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class pieDeFacturaAclinica(models.Model):
    factura = models.OneToOneField('FacturaAclinica',null=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)




