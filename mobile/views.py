from django.shortcuts import render, redirect, get_object_or_404
from medicamentos import models as Mmodels
from organizaciones import models as Omodels
from pedidos import models as Pmodels

from medicamentos.views import get_filtros as get_filtros_medicamentos


def VerMedicamentos(request):
    filters = get_filtros_medicamentos(request.GET, Mmodels.Medicamento)
    mfilters = dict(filter(lambda v: v[0] in Mmodels.Medicamento.FILTROS, filters.items()))
    medicamentos = Mmodels.Medicamento.objects.filter(**mfilters)
    estadisticas = {
        'total': Mmodels.Medicamento.objects.all().count(),
        'filtrados': medicamentos.count()
    }
    return render(request, "medicamentos_mobile.html", {"medicamentos": medicamentos, "filtros": filters, 'estadisticas': estadisticas})

def VerOrganizaciones(request):

    return render(request, "organizaciones_mobile.html")

def VerPedidos(request):

    return render(request, "pedidos_mobile.html")
