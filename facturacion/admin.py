from django.contrib import admin

from .models import Factura
from .models import DetalleFactura
from .models import pieDeFactura
from .models import formaDePago
from .models import Pago


class detalleFacturaLabTabularInline(admin.TabularInline):
    model = DetalleFactura

class pieDeFacturaTabularInline(admin.TabularInline):
    model = pieDeFactura

class FacturaAdmin(admin.ModelAdmin):
    inlines = [ detalleFacturaLabTabularInline,pieDeFacturaTabularInline ]



admin.site.register(Factura, FacturaAdmin)

admin.site.register(DetalleFactura)
admin.site.register(pieDeFactura)
admin.site.register(formaDePago)
admin.site.register(Pago)