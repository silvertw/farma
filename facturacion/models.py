from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from pedidos import config
from pedidos import models as pLabModel



class Factura(models.Model):
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


    #@property #Decorador que asigna signo pesos frente al precio unitario
    #def precioUnitario(self):
    #    return "$%s" % self.precioUnitario

    #@property #Decorador que asigna signo pesos frente al precio unitario
    #def importe(self):
    #    return "$%s" % self.importe

    #@property #Decorador que asigna signo pesos frente al precio unitario
    #def subtotal(self):
    #    return "$%s" % self.subtotal

class pieDeFactura(models.Model):

    factura = models.ForeignKey('Factura', null=True, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    #@property #Decorador que asigna signo pesos frente al precio unitario
    #def total(self):
    #    return "$%s" % self.total





