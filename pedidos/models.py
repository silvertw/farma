from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from pedidos import config
from django import utils

# ******************CLASES ABSTRACTAS******************#

class PedidoVenta(models.Model):
    FILTROS = "farmacia__razonSocial__icontains"
    nroPedido = models.AutoField(primary_key=True)
    fecha = models.DateField()


    class Meta:
        abstract = True

    def __str__(self):
        return str(self.nroPedido)


class DetallePedidoVenta(models.Model):
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1), 
                                           MaxValueValidator(config.MAXIMA_CANTIDAD_MEDICAMENTOS)])
    medicamento = models.ForeignKey('medicamentos.Medicamento')

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


# ******************REMITOS Y DETALLES REMITOS DE FARMACIA******************#

class RemitoDeFarmacia(models.Model):
    pedidoFarmacia = models.ForeignKey('PedidoDeFarmacia', on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return str(self.id)

    def to_json(self):
        if self.pk:
            return {
                'nroRemito': self.pk,
                'fecha': self.fecha
            }


class DetalleRemitoDeFarmacia(models.Model):
    remito = models.ForeignKey(RemitoDeFarmacia, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    detallePedidoDeFarmacia = models.ForeignKey('DetallePedidoDeFarmacia', on_delete=models.CASCADE)
    lote = models.ForeignKey('medicamentos.Lote')

    def __str__(self):
        return str(self.id)

    def set_detalle_pedido(self, detalle):
        self.detallePedidoDeFarmacia = detalle


# ******************REMITO Y DETALLES REMITO DE PEDIDO DE CLINICA******************#

class RemitoDeClinica(models.Model):
    pedidoDeClinica = models.ForeignKey('PedidoDeClinica', on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return str(self.id)

    def set_pedido(self, pedido):
        self.pedidoDeClinica = pedido

    def to_json(self):
        if self.pk:
            return {
                'nroRemito': self.pk,
                'fecha': self.fecha
            }


class DetalleRemitoDeClinica(models.Model):
    remito = models.ForeignKey('RemitoDeClinica', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    detallePedidoDeClinica = models.ForeignKey('DetallePedidoDeClinica', on_delete=models.CASCADE)
    lote = models.ForeignKey('medicamentos.Lote')

    def __str__(self):
        return str(self.id)

    def set_detalle_pedido(self, detalle):
        self.detallePedidoDeClinica = detalle


# ******************REMITO Y DETALLES REMITO DE DEVOLUCION DE MEDICAMENTOS VENCIDOS******************#

class RemitoMedicamentosVencidos(models.Model):
    numero = models.BigIntegerField()
    fecha = models.DateField()
    laboratorio = models.ForeignKey('organizaciones.Laboratorio', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.numero)

    def to_json(self):
        if self.laboratorio:
            return {'laboratorio': {'id': self.laboratorio.id,
                                 'razonSocial': self.laboratorio.razonSocial},
                    'fecha': datetime.datetime.now().strftime('%d/%m/%Y')}
        else:
            return {}

    def tiene_pedidoAlaboCon_remitoVencidosAsociado(self):
        try:
            valor = self.pedidoalaboratorio.tengo_remitos_de_vencidos()

        except Exception:
            return False
        return True



class DetalleRemitoMedicamentosVencido(models.Model):
    remito = models.ForeignKey('RemitoMedicamentosVencidos', on_delete=models.CASCADE)
    medicamento = models.ForeignKey('medicamentos.Medicamento')
    lote = models.ForeignKey('medicamentos.Lote')
    cantidad = models.PositiveIntegerField()
    dependencia = models.CharField(max_length=100)#Para saber de que farmacia provienen medicamentos
                                                              #vencidos.
    def __str__(self):
        return str(self.id)


# ******************REMITO Y DETALLES REMITO DE LABORATORIO******************#

class RemitoLaboratorio(models.Model):
    nroRemito = models.BigIntegerField(primary_key=True, unique=True)
    fecha = models.DateField()
    laboratorio = models.ForeignKey('organizaciones.Laboratorio', on_delete=models.CASCADE)
    pedidoLaboratorio = models.ForeignKey('PedidoAlaboratorio', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nroRemito)

    def to_json(self):
        if self.nroRemito:
            return {
                'nroRemito': self.nroRemito,
                'fecha': self.fecha
            }


class DetalleRemitoLaboratorio(models.Model):
    remito = models.ForeignKey('RemitoLaboratorio', on_delete=models.CASCADE)
    lote = models.ForeignKey('medicamentos.Lote')
    detallePedidoLaboratorio = models.ForeignKey('DetallePedidoAlaboratorio')
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


# ******************PEDIDO DE FARMACIA Y DETALLE PEDIDO DE FARMACIA******************#

class PedidoDeFarmacia(PedidoVenta):
    FILTROS = ["farmacia", "desde", "hasta","estado"]
    FILTERMAPPER = {
        'desde': "fecha__gte",
        'hasta': "fecha__lte",
        'farmacia': "farmacia__razonSocial__icontains",
        'estado': "estado__istartswith"
    }
    farmacia = models.ForeignKey('organizaciones.Farmacia', on_delete=models.CASCADE)
    estado = models.CharField(max_length=25, blank=True)
    tieneMovimientos = models.BooleanField(default=False)


    class Meta(PedidoVenta.Meta):
        verbose_name_plural = "Pedidos de Farmacia"
        permissions = (
            ("generar_reporte_farmacia", "Puede generar el reporte de pedidos a farmacia"),
        )

    def to_json(self):
        if self.farmacia:
            return {'farmacia': {'id': self.farmacia.id,
                                 'razonSocial': self.farmacia.razonSocial},
                    'fecha': self.fecha.strftime('%d/%m/%Y')}
        else:
            return {}

    def get_detalles(self):
        response = []
        if self.nroPedido:
            response = DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=self)
        return response

    def get_pendiente_total(self):
        detalles = DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=self)
        total=0
        for detalle in detalles:
            total += detalle.cantidadPendiente
        return total

    def get_disponible(self):
        detalles = DetallePedidoDeFarmacia.objects.filter(pedidoDeFarmacia=self)
        total=0
        for detalle in detalles:
            total += detalle.cantidad
        return total

    def get_pedidoFarmacia_nro(self,nroPedido):
        return PedidoDeFarmacia.objects.get(nroPedido=nroPedido)

    def get_instancia_es_mobile(self):
        return "no_mobile"


class DetallePedidoDeFarmacia(DetallePedidoVenta):
    pedidoDeFarmacia = models.ForeignKey('PedidoDeFarmacia', on_delete=models.CASCADE)
    cantidadPendiente = models.PositiveIntegerField(default=0)
    estaPedido = models.BooleanField(default=False)

    class Meta(DetallePedidoVenta.Meta):
        verbose_name_plural = "Detalles de Pedidos de Farmacia"

    def to_json(self):
        #para evitar acceder a campos nulos
        if self.medicamento:
            return {'medicamento': {"id": self.medicamento.id,
                                    "descripcion": self.medicamento.nombreFantasia.nombreF + " " +
                                                   self.medicamento.presentacion.descripcion + " " +
                                                   str(self.medicamento.presentacion.cantidad) + " " +
                                                   self.medicamento.presentacion.unidadMedida},
                    'cantidad': self.cantidad, 'cantidadPendiente': self.cantidadPendiente}
        else:
            return {}

    def set_pedido(self, pedido):
        self.pedidoDeFarmacia = pedido

class PedidoFarmaciaMobile(PedidoDeFarmacia):
    pedidoCerrado = models.BooleanField(default=False)
    notificado = models.BooleanField(default=False)

    def get_instancia_es_mobile(self):
        return "mobile"

# ******************PEDIDO DE CLINICA Y DETALLE PEDIDO DE CLINICA******************#

class PedidoDeClinica(PedidoVenta):
    FILTROS = ["desde", "hasta","obSoc","cliente"]
    FILTERMAPPER = {
        'desde': "fecha__gte",
        'hasta': "fecha__lte",
        'obSoc': "obraSocial__razonSocial__icontains",
        'cliente': "clinica__razonSocial__icontains"
    }
    clinica = models.ForeignKey('organizaciones.Clinica', on_delete=models.CASCADE)
    obraSocial = models.ForeignKey('organizaciones.ObraSocial', on_delete=models.CASCADE)
    medicoAuditor = models.CharField(max_length=80)
    facturaAsociada = models.BooleanField(default=False)

    class Meta(PedidoVenta.Meta):
        verbose_name_plural = "Pedidos de Clinica"

    def to_json(self):
        if self.clinica:
            return {'clinica': {'id': self.clinica.id,
                                 'razonSocial': self.clinica.razonSocial},
                    'fecha': self.fecha.strftime('%d/%m/%Y'),
                    'obraSocial': self.obraSocial.razonSocial,
                    'medicoAuditor': self.medicoAuditor}
        else:
            return {}

    def get_mi_factura(self):
        return self.facturaaclinica

    def get_factura_estado(self):#Si fuera foreyng key seria self.facturaaclinica__set pero al ser
                          #OneToOne no es necesario.
        return self.facturaaclinica.pagada


    def get_detalles(self):
        response = []
        if self.nroPedido:
            response = DetallePedidoDeClinica.objects.filter(pedidoDeClinica=self)
        return response


class DetallePedidoDeClinica(DetallePedidoVenta):
    pedidoDeClinica = models.ForeignKey('PedidoDeClinica', on_delete=models.CASCADE)
    cantidadPendiente = models.PositiveIntegerField(default=0)
    estaPedido = models.BooleanField(default=False)

    class Meta(DetallePedidoVenta.Meta):
        verbose_name_plural = "Detalles de Pedidos de Clinica"

    def to_json(self):
        #para evitar acceder a campos nulos
        if self.medicamento:
            return {'medicamento': {"id": self.medicamento.id,
                                    "descripcion": self.medicamento.nombreFantasia.nombreF + " " +
                                                   self.medicamento.presentacion.descripcion + " " +
                                                   str(self.medicamento.presentacion.cantidad) + " " +
                                                   self.medicamento.presentacion.unidadMedida},
                    'cantidad': self.cantidad}
        else:
            return {}

    def set_pedido(self, pedido):
        self.pedidoDeClinica = pedido


# ================================================ PEDIDO A LABORATORIO ================================================

# PEDIDO A LABORATORIO

class PedidoAlaboratorio(models.Model):
    FILTROS = ["laboratorio", "desde", "hasta"]
    FILTERMAPPER = {
        'laboratorio': "laboratorio__razonSocial__icontains",
        'desde': "fecha__gte",
        'hasta': "fecha__lte"
    }
    nroPedido = models.AutoField(primary_key=True)
    fecha = models.DateField(auto_now_add=True)
    laboratorio = models.ForeignKey('organizaciones.Laboratorio', on_delete=models.CASCADE)
    estado = models.CharField(max_length=25, blank=True, default="Pendiente")# cancelado, parcialmente recibido, pendiente, completo
    facturaAsociada = models.BooleanField(default=False)
    #Si es un pedido realizado con el fin de cubrir la quita de medicamentos vencidos, se
    #asocia el remito que da detalle de donde provienen esos medicamentos vencidos.
    remitoVencidosAsociado = models.OneToOneField('RemitoMedicamentosVencidos',blank=True,null=True)


    def __str__(self):
        return 'Pedido Nro %s - Laboratorio: %s' % (self.nroPedido, self.laboratorio)
    
    def to_json(self):
        if self.laboratorio:
            return {'laboratorio': {'id': self.laboratorio.id,
                                 'razonSocial': self.laboratorio.razonSocial},
                    'fecha': datetime.datetime.now().strftime('%d/%m/%Y')}
        else:
            return {}

    def get_detalles(self):
        response = []
        if self.nroPedido:
            response = DetallePedidoAlaboratorio.objects.filter(pedido=self)
        return response

    def tengo_remitos_de_vencidos(self):
        if self.remitoVencidosAsociado:
            return True
        else:
            return False

# DETALLE PEDIDO A LABORATORIO

class DetallePedidoAlaboratorio(models.Model):
    renglon = models.AutoField(primary_key=True)
    pedido = models.ForeignKey('PedidoAlaboratorio', null=True, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1), 
                                           MaxValueValidator(config.MAXIMA_CANTIDAD_MEDICAMENTOS)])
    cantidadPendiente = models.PositiveIntegerField()
    medicamento = models.ForeignKey('medicamentos.Medicamento')
    detallePedidoFarmacia = models.ForeignKey('DetallePedidoDeFarmacia', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Pedido Nro %s - Detalle %s"%(self.pedido.nroPedido, self.renglon)
    
    def to_json(self):
        response = {}

        # para evitar acceder a campos nulos
        if self.renglon:
            response['renglon'] = self.renglon

        # para evitar acceder a campos nulos
        if self.medicamento:
            response['medicamento'] = {"id": self.medicamento.id,
                                       "descripcion": self.medicamento.nombreFantasia.nombreF + " " +
                                                   self.medicamento.presentacion.descripcion + " " +
                                                   str(self.medicamento.presentacion.cantidad) + " " +
                                                   self.medicamento.presentacion.unidadMedida }

        if self.detallePedidoFarmacia:
            response['detallePedidoFarmacia'] = self.detallePedidoFarmacia.pk
        else:
            response['detallePedidoFarmacia'] = -1

        response['cantidad'] = self.cantidad
        response['cantidadPendiente'] = self.cantidadPendiente
        return response

class movimientosDeStockDistribuido(models.Model):
    farmaciaDeDestino = models.CharField(max_length=50)
    fecha=models.DateField(default=utils.timezone.now)
    pedidoMov=models.ForeignKey('PedidoDeFarmacia')

    def ultimoPk(self):
        ultimo = len(self)
        return ultimo

    def get_detalles_movimientos(self):
        return self.detalledemovimientos

    def get_movimiento_pedidoFarm(self,pedidoDeFarmacia):
        return movimientosDeStockDistribuido.objects.get(pedidoMov=pedidoDeFarmacia)

    def __str__(self):
        return 'Farmacia de Destino: %s' % (self.farmaciaDeDestino)

class detalleDeMovimientos(models.Model):
    movimiento = models.ForeignKey('movimientosDeStockDistribuido', null=True, on_delete=models.CASCADE)
    farmacia = models.CharField(max_length=50)
    lote = models.PositiveIntegerField()
    cantidadQuitada = models.PositiveIntegerField()


