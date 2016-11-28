from django.contrib import admin

from .models import FacturaDeProveedor
from .models import DetalleFacturaDeProveedor
from .models import pieDeFacturaDeProveedor

from .models import FacturaAclinica
from .models import DetalleFacturaAclinica
from .models import pieDeFacturaAclinica

from .models import formaDePago
from .models import Pago


class detalleFacturaLabTabularInline(admin.TabularInline):
    model = DetalleFacturaDeProveedor

class pieDeFacturaTabularInline(admin.TabularInline):
    model = pieDeFacturaDeProveedor

class FacturaAdmin(admin.ModelAdmin):
    inlines = [ detalleFacturaLabTabularInline,pieDeFacturaTabularInline ]

#=============================================================================================

class detalleFacturaAclinicaTabularInline(admin.TabularInline):
    model = DetalleFacturaAclinica

class pieDeFacturaAclinicaTabularInline(admin.TabularInline):
    model = pieDeFacturaAclinica

class FacturaAclinicaAdmin(admin.ModelAdmin):
    inlines = [ detalleFacturaAclinicaTabularInline,pieDeFacturaAclinicaTabularInline ]

admin.site.register(FacturaDeProveedor, FacturaAdmin)
admin.site.register(FacturaAclinica, FacturaAclinicaAdmin)

admin.site.register(DetalleFacturaDeProveedor)
admin.site.register(pieDeFacturaDeProveedor)

admin.site.register(DetalleFacturaAclinica)
admin.site.register(pieDeFacturaAclinica)

admin.site.register(formaDePago)
admin.site.register(Pago)