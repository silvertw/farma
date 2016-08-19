from django.contrib import admin
from .models import Farmacia, Clinica, Laboratorio, ObraSocial
from medicamentos.models import Medicamento


class MedicamentoTabularInline(admin.TabularInline):
    model = Medicamento


class ObraSocialTabularInline(admin.TabularInline):
    model = ObraSocial

class LaboratorioAdmin(admin.ModelAdmin):
    inlines = [MedicamentoTabularInline]


class ClinicaAdmin(admin.ModelAdmin):
    inlines = [ObraSocialTabularInline]

admin.site.register(Farmacia)
admin.site.register(Clinica)
admin.site.register(Laboratorio, LaboratorioAdmin)
admin.site.register(ObraSocial)
