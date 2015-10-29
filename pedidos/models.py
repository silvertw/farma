from django.db import models

# Create your models here.
class RemitoMedVencido(models.Model):
    FILTROS = ["numero__icontains"]
    numero = models.BigIntegerField()
    fecha = models.DateField()
    #estado
    def __str__(self):
        return self.numero


class DetalleRemitoVencido(models.Model):
    FILTROS = ["numero__icontains"]
    numeroRemito = models.ForeignKey('RemitoMedVencido',on_delete = models.CASCADE)
    cantidad = models.BigIntegerField()
    #estado
    def __str__(self):
        return self.numero

#CLASE ABSTRACTA PEDIDO VENTA
class PedidoVenta(models.Model):
    nroPedido = models.AutoField(primary_key=True)
    fecha = models.DateField(editable=True)

    class Meta:
        abstract = True


#CLASE ABSTRACTA DETALLE PEDIDO
class DetallePedido(models.Model):
    renglon = models.AutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    medicamento = models.ForeignKey('medicamentos.Medicamento')

    class Meta:
        abstract = True

#PEDIDO DE FARMACIA
class PedidoFarmacia(PedidoVenta):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('parcialmente enviado', 'Parcialmente enviado'),
        ('enviado', 'Enviado'),
    )
    farmacia = models.ForeignKey('organizaciones.Farmacia')
    estado = models.CharField(max_length=25, choices=ESTADOS)

#DETALLE PEDIDO DE FARMACIA

class DetallePedidoFarmacia(DetallePedido):
    pedidoFarmacia = models.ForeignKey('PedidoFarmacia')