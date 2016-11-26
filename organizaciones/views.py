#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from organizaciones import models, forms, utils
from django.contrib.auth.decorators import login_required
from jsonview.decorators import json_view
from django.contrib.auth.decorators import permission_required
from pedidos import models as pmodels
from django.http import HttpResponse
import json
from xlsxwriter import Workbook
from collections import OrderedDict
import io

def get_filtros(get, modelo):
    mfilter = {}
    for filtro in modelo.FILTROS:
        attr = filtro.split("__")[0]
        if attr in get and get[attr]:
            mfilter[filtro] = get[attr]
            mfilter[attr] = get[attr]
    return mfilter


def hubo_alta(session):
    if 'successAdd' in session:
        del session['successAdd']
        return True
    return False
    
# ****** FARMACIAS ******


@login_required(login_url='login')
def farmacias(request):
    # type: (object) -> object
    """

    :rtype: object
    """
    filters = get_filtros(request.GET, models.Farmacia)
    mfilters = dict(filter(lambda v: v[0] in models.Farmacia.FILTROS, filters.items()))
    lfarmacias = models.Farmacia.objects.filter(**mfilters)
    estadisticas = {
        'total': models.Farmacia.objects.all().count(),
        'filtrados': lfarmacias.count()
    }
    return render(request, "farmacia/farmacias.html", {"farmacias": lfarmacias, "filtros": filters, 'estadisticas': estadisticas})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def farmacia_add(request):
    if request.method == "POST":
        form = forms.FarmaciaFormAdd(request.POST)

        if form.is_valid():
            form.save()
            if '_volver' in request.POST:
                return redirect('farmacias')
            else:
                request.session['successAdd'] = True
                return redirect('farmacia_add')
    else:
        form = forms.FarmaciaFormAdd()
    successAdd = hubo_alta(request.session)
    return render(request, "farmacia/farmaciaAdd.html", {"form": form, 'successAdd': successAdd})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def farmacia_update(request, id_farmacia):
    farmacia = get_object_or_404(models.Farmacia, pk=id_farmacia)
    if request.method == "POST":
        form = forms.FarmaciaFormUpdate(request.POST, instance=farmacia)
        if form.is_valid():
            form.save()
            return redirect('farmacias')
    else:
        form = forms.FarmaciaFormUpdate(instance=farmacia)
    return render(request, "farmacia/farmaciaUpdate.html", {'form': form, 'farmacia': farmacia})


@json_view
@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def farmacia_try_delete(request, id_farmacia):
    infoBaja = utils.puedo_eliminar_farmacia(id_farmacia)
    return infoBaja


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def farmacia_delete(request, id_farmacia):
    infoBaja = utils.puedo_eliminar_farmacia(id_farmacia)
    if infoBaja['success']:
        farmacia = get_object_or_404(models.Farmacia, pk=id_farmacia)
        pedidosAlaboratorio = set()
        pedidosDeFarmacia = pmodels.PedidoDeFarmacia.objects.filter(farmacia=farmacia)
        for pedido in pedidosDeFarmacia:
            detallesPedidoDeFarmacia = pedido.get_detalles()
            for detalle in detallesPedidoDeFarmacia:
                detallesPedidoAlaboratorio = pmodels.DetallePedidoAlaboratorio.objects.filter(detallePedidoFarmacia=detalle)
                for detallePedidoAlaboratorio in detallesPedidoAlaboratorio:
                    pedidosAlaboratorio.add(detallePedidoAlaboratorio.pedido)

        for pedido in pedidosAlaboratorio:
            if pedido.get_detalles().count() <= 1:
                p = pmodels.PedidoAlaboratorio.objects.get(pk=pedido.pk)
                p.delete()

        farmacia.delete()
        return redirect('farmacias')


# ****** CLINICAS ******

@login_required(login_url='login')
def clinicas(request):
    filters = get_filtros(request.GET, models.Clinica)
    mfilters = dict(filter(lambda v: v[0] in models.Clinica.FILTROS, filters.items()))
    lclinicas = models.Clinica.objects.filter(**mfilters)
    estadisticas = {
        'total': models.Clinica.objects.all().count(),
        'filtrados': lclinicas.count()
    }
    return render(request, "clinica/clinicas.html", {"clinicas": lclinicas, "filtros": filters, 'estadisticas': estadisticas})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def clinica_add(request):
    if request.method == "POST":
        form = forms.ClinicaFormAdd(request.POST)
        if form.is_valid(): 
            form.save()
            if '_volver' in request.POST:
                return redirect('clinicas')
            else:
                request.session['successAdd'] = True
                return redirect('clinica_add')
    else:
        form = forms.ClinicaFormAdd()
    successAdd = hubo_alta(request.session)
    return render(request, "clinica/clinicaAdd.html", {"form": form, 'successAdd': successAdd})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def clinica_update(request, id_clinica):
    clinica = get_object_or_404(models.Clinica, pk=id_clinica)
    if request.method == "POST":
        form = forms.ClinicaFormUpdate(request.POST, instance=clinica)
        if form.is_valid():
            form.save()
            return redirect('clinicas')
    else:
        form = forms.ClinicaFormUpdate(instance=clinica)
    return render(request, "clinica/clinicaUpdate.html", {'form': form, 'clinica': clinica})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def clinica_delete(request, id_clinica):
    clinica = models.Clinica.objects.get(pk=id_clinica)

    pedidosDeClinica = pmodels.PedidoDeClinica.objects.filter(clinica=clinica)
    for pedido in pedidosDeClinica:
        pedido.delete()

    clinica.delete()
    return redirect('clinicas')


# ******* LABORATORIOS ******

@login_required(login_url='login')
def laboratorios(request):
    filters = get_filtros(request.GET, models.Laboratorio)
    mfilters = dict(filter(lambda v: v[0] in models.Laboratorio.FILTROS, filters.items()))
    llaboratorios = models.Laboratorio.objects.filter(**mfilters)
    estadisticas = {
        'total': models.Laboratorio.objects.all().count(),
        'filtrados': llaboratorios.count()
    }
    return render(request, "laboratorio/laboratorios.html",{"laboratorios": llaboratorios, "filtros": filters, 'estadisticas': estadisticas})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def laboratorio_add(request):
    if request.method == "POST":
        form = forms.LaboratorioFormAdd(request.POST)
        if form.is_valid():    
            form.save()
            if '_volver' in request.POST:
                return redirect('laboratorios')
            else:
                request.session['successAdd'] = True
                return redirect('laboratorio_add')
    else:
        form = forms.LaboratorioFormAdd()
    successAdd = hubo_alta(request.session)
    return render(request, "laboratorio/laboratorioAdd.html", {"form": form, 'successAdd': successAdd})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def laboratorio_update(request, id_laboratorio):
    laboratorio = get_object_or_404(models.Laboratorio, pk=id_laboratorio)
    if request.method == "POST":
        form = forms.LaboratorioFormUpdate(request.POST, instance=laboratorio)
        if form.is_valid():
            form.save()
            return redirect('laboratorios')
    else:
        form = forms.LaboratorioFormUpdate(instance=laboratorio)
    return render(request, "laboratorio/laboratorioUpdate.html", {'form': form, 'laboratorio': laboratorio})


@json_view
@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def laboratorio_try_delete(request, id_laboratorio):
    infoBaja = utils.puedo_eliminar_laboratorio(id_laboratorio)
    return infoBaja

@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def laboratorio_delete(request, id_laboratorio):
    infoBaja = utils.puedo_eliminar_laboratorio(id_laboratorio)
    if infoBaja['success']:
        laboratorio = models.Laboratorio.objects.get(pk=id_laboratorio)
        pedidosAlaboratorio = pmodels.PedidoAlaboratorio.objects.filter(laboratorio=laboratorio)
        for pedido in pedidosAlaboratorio:
            pedido.delete()

        laboratorio.delete()
        return redirect('laboratorios')

# ******* OBRAS SAOCIALES ******

@login_required(login_url='login')
def ObrasSociales(request):
    filters = get_filtros(request.GET, models.ObraSocial)
    mfilters = dict(filter(lambda v: v[0] in models.ObraSocial.FILTROS, filters.items()))
    lObrasSociales = models.ObraSocial.objects.filter(**mfilters)
    estadisticas = {
        'total': models.ObraSocial.objects.all().count(),
        'filtrados': lObrasSociales.count()
    }
    return render(request, "obraSocial/ObrasSociales.html", {"ObrasSociales": lObrasSociales, "filtros": filters, 'estadisticas': estadisticas})

@login_required(login_url='login')
def ObSocAdjuntarAclinica(request, id_clinica):

    clinica = models.Clinica.objects.get(pk=id_clinica)
    lObSoc=(models.ObraSocial.objects.filter(clinica__pk=id_clinica))#obteniendo objetos de la relacion
    filters = get_filtros(request.GET, models.ObraSocial)
    mfilters = dict(filter(lambda v: v[0] in models.ObraSocial.FILTROS, filters.items()))
    lObrasSociales = lObSoc.filter(**mfilters)

    print "OBRAS SOCIALES1-->",lObSoc
    print "OBRAS SOCIALES2-->",lObrasSociales

    estadisticas = {
        'total': models.ObraSocial.objects.all().count(),
        'filtrados': lObrasSociales.count()
    }
    return render(request, "obraSocial/ObSocAdjuntarAclinica.html", {"ObrasSociales": lObrasSociales, "filtros": filters, 'estadisticas': estadisticas, "clinica":clinica})

@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def obraSocial_add(request):
    if request.method == "POST":
        form = forms.ObraSocialFormAdd(request.POST)
        if form.is_valid():
            form.save()
            if '_volver' in request.POST:
                return redirect('ObrasSociales')
            else:
                request.session['successAdd'] = True
                return redirect('obraSocial_add')
    else:
        form = forms.ObraSocialFormAdd()
    successAdd = hubo_alta(request.session)
    return render(request, "obraSocial/obraSocialAdd.html", {"form": form, 'successAdd': successAdd})

@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def obraSocial_update(request, id_obraSocial):
    obraSocial = get_object_or_404(models.ObraSocial, pk=id_obraSocial)
    if request.method == "POST":
        form = forms.ObraSocialFormUpdate(request.POST, instance=obraSocial)
        if form.is_valid():
            form.save()
            return redirect('ObrasSociales')
    else:
        form = forms.ObraSocialFormUpdate(instance=obraSocial)
    return render(request, "obraSocial/obraSocialUpdate.html", {'form': form, 'obraSocial': obraSocial})


def ObSocAdjuntarAclinicaR (request):


    var = request.GET #Se otiene el request
    data_request = var.keys()#Obtiene el JSON del request
    decoded_json = json.loads(data_request[0])#Decodificacion de JSON

    #================SE OBTIENE CADA VALOR=======================
    idDeClin = decoded_json["idDeClin"]
    RazonSocClin = decoded_json["razSocClinAenviar"]
    razonSocialOS = decoded_json["razSocOsAenviar"]

    clinicaObject = models.Clinica.objects.get(pk=idDeClin)#Se obtiene el objeto clinica
    lObSocAll = models.ObraSocial.objects.all()#Se obtienen todas las obras sociales existentes
    lObSoc = (models.ObraSocial.objects.filter(clinica__pk=idDeClin))#Se obtienen todos las ob soc que estan relacionadas a la clinica actual

    obSocTodas = lObSocAll.filter(razonSocial=razonSocialOS)#Obtiene la obra social de todas las existentes
    obSocClinica = lObSoc.filter(razonSocial=razonSocialOS)#Obtiene la obra social de todas las que estan vinculadas a la clinica

    if obSocTodas:
        if obSocClinica:
            #----------------------------------------------------------
            if decoded_json["action"]=="desvincular":
                IdObraSocial = decoded_json["idDeObraSocial"]
                ObSocRemov = models.ObraSocial.objects.get(pk=IdObraSocial)
                clinicaObject.obraSocial.remove(ObSocRemov)
            else:
                msj = "La obra social ya esta vinculada a esta Clinica"
            #----------------------------------------------------------
        else:

            clinicaObject.obraSocial.add(obSocTodas[0])
            clinicaObject.save()

            msj="La Obra Social se vinculo correctamente"
    else:
        msj = "La obra social que intenta vincular no existe"

    response = HttpResponse(msj)

    return response







