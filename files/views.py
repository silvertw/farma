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
        invalid=False
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            datos = form.cleaned_data["docfile"].read()

            #============================PROCESAMIENTO DEL ARCHIVO============================================

            farmacias=omodels.Farmacia.objects.all()#Obtiene todas las farmacias.
            nombresFarmaias=[]

            for farm in farmacias:
                nombresFarmaias.append(farm.razonSocial)#Guarda sus razones sociales en una lista.

            fecha = re.compile(r'^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[012])/((19|20)\d\d)$')#Exp. reg. para validar fecha

            #------------------------------------RECORRIDO PARA VALIDAR---------------------------------------
            i=0
            listaLineas=[]
            listaErrores=[]
            for linea in datos.splitlines():
                parDeValores=linea.split('_')

                if i==0:#Primer linea para validar farmacia y fecha
                    farmacia=parDeValores[0]
                    if not parDeValores[0] in nombresFarmaias:#Verifica que el nombre de farmacia del archivo sea
                                                               #correcto y sea de una farmacia activa.
                        invalid=True
                    if fecha.search(parDeValores[1]) is None:#Verifica que la cadena fecha sea correcta
                        invalid=True
                else:

                    if not parDeValores[0].isdigit():
                        invalid=True
                    if not parDeValores[1].isdigit():
                        invalid=True

                    listaLineas.append(linea)

                i += 1
            #--------------------------RECORIDO PARA DESCONTAR SI EL ARCHIVO ES VALIDO-----------------------------
            if not invalid:
                for linea in listaLineas:
                    parDeValores=linea.split('_')
                    lote=parDeValores[0]
                    cantidad=parDeValores[1]
                    buscarLotesYdescontarStock(farmacia,lote,cantidad)
                    invalid="Procesado"
        else:
            invalid=True
    else:
        form = UploadForm()
        invalid=False
    return render(request, "uploadFile.html", {'form': form,'invalid':invalid})

def buscarLotesYdescontarStock(farmacia,lote,cantidad):
    stockDist=mmodels.StockDistribuidoEnFarmacias.objects.filter(lote__numero=lote,farmacia__razonSocial=farmacia)

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













