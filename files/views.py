from django.shortcuts import render
from django.shortcuts import render, redirect #puedes importar render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from files.forms import UploadForm
from files.models import Document
from organizaciones import models as omodels
from medicamentos import models as mmodels
from files import models as fmodels
import os
import re
import time
import datetime

@permission_required('usuarios.encargado_de_farmacia', login_url='login')
@login_required(login_url='login')
def uploadFile(request):
    if request.method == 'POST':
        fechaActual = time.strftime("%d/%m/%Y")
        fechaActual = datetime.datetime.strptime(fechaActual, '%d/%m/%Y').date()

        estado=True
        form = UploadForm(request.POST, request.FILES)

        if not(fmodels.Document.objects.filter(fechaUpload=fechaActual).exists()):

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

                        fechaArchivo = datetime.datetime.strptime(parDeValores[1], '%d/%m/%Y').date()

                        if (fecha.search(parDeValores[1]) is None):#Verifica que la cadena fecha sea correcta
                            estado=False

                        if (fechaActual != fechaArchivo):
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
                    i=0
                    estadoBusqueda=True
                    while i < len(listaLineas) and estadoBusqueda:
                        parDeValores=listaLineas[i].split(',')
                        lote=parDeValores[0]
                        cantidad=parDeValores[1]
                        estadoBusqueda=buscarLotesYdescontarStock(pkFarmacia,lote,cantidad)
                        i += 1
                    if estadoBusqueda:
                        docUpload=fmodels.Document(
                            fechaUpload=fechaActual
                        )
                        docUpload.save()
                    else:
                       estado=False

            else:
                estado=False
        else:
            estado=False
    else:
        form = UploadForm()
        estado=None
    return render(request, "uploadFile.html", {'form': form,'estado':estado})

def buscarLotesYdescontarStock(pkFarmacia,lote,cantidad):

    stockDist=mmodels.StockDistribuidoEnFarmacias.objects.filter(lote__numero=lote,farmacia__pk=pkFarmacia)
    cantidad=int(cantidad)
    estadoBusqueda=True

    for sd in stockDist:
        if ( (sd.cantidad >= cantidad) and (cantidad >=0) ):
            sd.cantidad -= cantidad
            sd.save()
            if( (sd.cantidad == 0)and(sd.lote.stock == 0) ):
                loteObj=mmodels.Lote.objects.get(numero=lote)
                loteObj.delete()
                sd.delete()

            stockFYF = sd.lote.stockFarmaYfarmacias
            stockFYF.stockFarmacias -= cantidad
            stockFYF.save()
        else:
            estadoBusqueda=False

    return estadoBusqueda




