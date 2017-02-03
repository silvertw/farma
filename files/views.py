from django.shortcuts import render
from django.shortcuts import render, redirect #puedes importar render_to_response
from files.forms import UploadForm
from files.models import Document
from organizaciones import models as omodels
from medicamentos import models as mmodels
import os
import re

def uploadFile(request):
    if request.method == 'POST':
        estado=True
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            datos = form.cleaned_data["docfile"].read()

            #============================PROCESAMIENTO DEL ARCHIVO============================================

            farmacias=omodels.Farmacia.objects.all()#Obtiene todas las farmacias.
            pkFarmacias=[]

            for farm in farmacias:
                pkFarmacias.append(farm.pk)#Guarda sus razones sociales en una lista.

            fecha = re.compile(r'^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/((19|20)\d\d)$')#Exp. reg. para validar fecha

            #------------------------------------RECORRIDO PARA VALIDAR---------------------------------------
            i=0
            listaLineas=[]

            for linea in datos.splitlines():
                parDeValores=linea.split(',')

                if i==0:#Primer linea para validar farmacia y fecha
                    pkFarmacia = int(parDeValores[0])

                    if not pkFarmacia in pkFarmacias:#Verifica que el pk de farmacia del archivo sea
                                                               #correcto y sea de una farmacia activa.

                        estado=False
                    if fecha.search(parDeValores[1]) is None:#Verifica que la cadena fecha sea correcta
                        estado=False
                else:

                    if not parDeValores[0].isdigit():
                        estado=False
                    if not parDeValores[1].isdigit():
                        estado=False

                    listaLineas.append(linea)

                i += 1
            #--------------------------RECORRIDO PARA DESCONTAR SI EL ARCHIVO ES VALIDO-----------------------------
            if estado:
                for linea in listaLineas:
                    parDeValores=linea.split(',')
                    lote=parDeValores[0]
                    cantidad=parDeValores[1]
                    buscarLotesYdescontarStock(pkFarmacia,lote,cantidad)

        else:
            estado=False
    else:
        form = UploadForm()
        estado=None
    return render(request, "uploadFile.html", {'form': form,'estado':estado})

def buscarLotesYdescontarStock(pkFarmacia,lote,cantidad):
    stockDist=mmodels.StockDistribuidoEnFarmacias.objects.filter(lote__numero=lote,farmacia__pk=pkFarmacia)

    totalQuitado=0
    cantidad=int(cantidad)
    for sd in stockDist:
        totalQuitado += cantidad
        stockFYF = sd.lote.stockFarmaYfarmacias
        stockFYF.stockFarmacias -= cantidad
        stockFYF.save()
        sd.cantidad -= cantidad
        lote = sd.lote
        lote.stock -= cantidad
        lote.save()
        sd.save()













