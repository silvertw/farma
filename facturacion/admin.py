from django.contrib import admin

from .models import Factura
from .models import DetalleFactura

class detalleFacturaLabTabularInline(admin.TabularInline):
    model = DetalleFactura


class FacturaAdmin(admin.ModelAdmin):
    inlines = [ detalleFacturaLabTabularInline ]

admin.site.register(Factura, FacturaAdmin)
admin.site.register(DetalleFactura)
