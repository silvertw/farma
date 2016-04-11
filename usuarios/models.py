from django.db import models
from django.contrib.auth.models import User
from . import choices

# Create your models here.
class Usuario(User):

	cargo = models.CharField(max_length=50, choices=choices.CARGO_CHOICES)

	class Meta:
		permissions = (
 			("encargado_general", 'Cargo de encargado general'),
 			("encargado_medicamentos_vencidos", "Cargo de encargado de medicamentos vencidos"),
 			("encargado_stock", "Cargo Encargado de stock"),
 			("encargado_pedido", "Cargo Encargado de pedido"),
 			("empleado_despacho_pedido", "Cargo Encargado de despacho de pedido")
 		)









	"""CARGO_CHOICES = (
		('Encargado General', 'Encargado General'),
		('Encargado Medicamentos Vencidos', 'Encargado Medicamentos Vencidos'),
		('Encargado de Stock', 'Encargado de Stock'),
		('Encargado de Pedido', 'Encargado de Pedido'),
		('Empleado de Despacho de Pedido', 'Empleado de Despacho de Pedido'),
	)"""