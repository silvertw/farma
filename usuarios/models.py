from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from . import choices
from organizaciones import models as orgmodels


class Usuario(AbstractUser):
    cargo = models.CharField(max_length=50, choices=choices.CARGO_CHOICES)
    farmacia = models.ForeignKey(orgmodels.Farmacia, null=True, blank=True)

    class Meta:
        permissions = (
            ("encargado_general", 'Cargo de encargado general'),
            ("encargado_medicamentos_vencidos", "Cargo de encargado de medicamentos vencidos"),
            ("encargado_stock", "Cargo Encargado de stock"),
            ("encargado_pedido", "Cargo Encargado de pedido"),
            ("empleado_despacho_pedido", "Cargo Encargado de despacho de pedido"),
            ("encargado_de_farmacia", "Cargo Responsable de Farmacia")
        )