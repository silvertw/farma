from django.contrib import admin

from .models import Factura
from .models import DetalleFactura
from .models import pieDeFactura

from .models import FacturaAclinica
from .models import DetalleFacturaAclinica
from .models import pieDeFacturaAclinica

from .models import formaDePago
from .models import Pago


class detalleFacturaLabTabularInline(admin.TabularInline):
    model = DetalleFactura

class pieDeFacturaTabularInline(admin.TabularInline):
    model = pieDeFactura

class FacturaAdmin(admin.ModelAdmin):
    inlines = [ detalleFacturaLabTabularInline,pieDeFacturaTabularInline ]

#=============================================================================================

class detalleFacturaAclinicaTabularInline(admin.TabularInline):
    model = DetalleFacturaAclinica

class pieDeFacturaAclinicaTabularInline(admin.TabularInline):
    model = pieDeFacturaAclinica

class FacturaAclinicaAdmin(admin.ModelAdmin):
    inlines = [ detalleFacturaAclinicaTabularInline,pieDeFacturaAclinicaTabularInline ]

admin.site.register(Factura, FacturaAdmin)
admin.site.register(FacturaAclinica, FacturaAclinicaAdmin)

admin.site.register(DetalleFactura)
admin.site.register(pieDeFactura)

admin.site.register(DetalleFacturaAclinica)
admin.site.register(pieDeFacturaAclinica)

admin.site.register(formaDePago)
admin.site.register(Pago)