from django.shortcuts import render, redirect, get_object_or_404
from medicamentos import models as Mmodels
from organizaciones import models as Omodels
from pedidos import models as Pmodels

from pedidos.views import get_filtros as get_filtros_pedidos, get_filtros

def VerMedicamentos(request):
    filters = get_filtros(request.GET, Mmodels.Medicamento)
    mfilters = dict(filter(lambda v: v[0] in Mmodels.Medicamento.FILTROS, filters.items()))
    medicamentos = Mmodels.Medicamento.objects.filter(**mfilters)
    estadisticas = {
        'total': Mmodels.Medicamento.objects.all().count(),
        'filtrados': medicamentos.count()
    }
    return render(request, "medicamentos_mobile.html", {"medicamentos": medicamentos, "filtros": filters, 'estadisticas': estadisticas})

def VerOrganizaciones(request):
    filters = get_filtros(request.GET, Omodels.Organizacion)
    mfilters = dict(filter(lambda v: v[0] in Omodels.Organizacion.FILTROS, filters.items()))
    organizacionesFarmacia = Omodels.Farmacia.objects.filter(**mfilters)
    organizacionesClinica = Omodels.Clinica.objects.filter(**mfilters)
    organizacionesObraSocial = Omodels.ObraSocial.objects.filter(**mfilters)
    organizacionesLaboratorio = Omodels.Laboratorio.objects.filter(**mfilters)
    return render(request, "organizaciones_mobile.html", {"organizacionesFarmacia": organizacionesFarmacia, "organizacionesClinica": organizacionesClinica, "organizacionesObraSocial": organizacionesObraSocial, "organizacionesLaboratorio": organizacionesLaboratorio})

def VerPedidos(request):
    filters = get_filtros_pedidos(request.GET, Pmodels.PedidoVenta)
    mfilters = dict(filter(lambda v: v[0] in Pmodels.PedidoVenta.FILTROS, filters.items()))
    pedidosFarm = Pmodels.PedidoDeFarmacia.objects.filter(**mfilters)
    return render(request, "pedidos_mobile.html", {"pedidosFarm": pedidosFarm})

def MostrarMedicamento(request, id_medicamento):
    medicamento = Mmodels.Medicamento.objects.get(pk=id_medicamento)
    return render(request, "mostrar_medicamento_mobile.html", {"medicamento": medicamento})

def informacionMobile(request):
    return render(request, "informacion_mobile.html")

def MostrarPedido(request, id_pedido):
    pedido = Pmodels.PedidoDeFarmacia.objects.get(pk=id_pedido)
    return render(request, "mostrar_pedidos_mobile.html", {"pedido": pedido})

def MostrarOrganizacionFarmacia(request, id_organizacion):
    organizacion = Omodels.Farmacia.objects.get(pk=id_organizacion)
    return render(request, "mostrar_organizacion_mobile.html", {"organizacion": organizacion})

def MostrarOrganizacionClinica(request, id_organizacion):
    organizacion = Omodels.Clinica.objects.get(pk=id_organizacion)
    return render(request, "mostrar_organizacion_mobile.html", {"organizacion": organizacion})

def MostrarOrganizacionObSoc(request, id_organizacion):
    organizacion = Omodels.ObraSocial.objects.get(pk=id_organizacion)
    return render(request, "mostrar_organizacion_mobile.html", {"organizacion": organizacion})

def MostrarOrganizacionLaboratorio(request, id_organizacion):
    organizacion = Omodels.Laboratorio.objects.get(pk=id_organizacion)
    return render(request, "mostrar_organizacion_mobile.html", {"organizacion": organizacion})

def PedirMedicamento(request, id_medicamento):
    medicamento = Mmodels.Medicamento.objects.get(pk=id_medicamento)

    filters = get_filtros_pedidos(request.GET, Pmodels.PedidoVenta)
    mfilters = dict(filter(lambda v: v[0] in Pmodels.PedidoVenta.FILTROS, filters.items()))
    pedidosFarm = Pmodels.PedidoDeFarmacia.objects.filter(**mfilters)

    return render(request, "pedir_medicamento_mobile.html", {"medicamento": medicamento, "pedidosFarm": pedidosFarm})



def CrearPedido(request):
    print "VOY A CREAR!"
    return render(request, "pedir_medicamento_mobile.html", {})





