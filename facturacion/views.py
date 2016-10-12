
from django.shortcuts import render, redirect, get_object_or_404
import models, forms
from django.contrib.auth.decorators import login_required
from jsonview.decorators import json_view
from django.contrib.auth.decorators import permission_required
from pedidos import models as pmodels
from django.db import transaction
from medicamentos import models as medmodels
import models as factmodels
from pedidos.views import get_filtros as get_filtros_pedidos
from pedidos import utils as putils
from django.http import HttpResponse
import json

# Create your views here.

def facturacionVentas(request):

    return render(request,"ClinicasYobrasSociales/facturacionVentas.html",{})

@transaction.atomic
def facturacionCompras(request):
    erroresEnElForm = "False"
    nroPedidoAlab=0

    if request.method == "POST":

        form = forms.RegistrarFactura(request.POST)
        if form.is_valid():

            #==================Logica para crear factura======================

            factura = form.save(commit=False)
            listaDetallesFactura=[]

            nroPedido = request.session['nroPedidoAlab']
            pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedido)
            detallesPedido = pmodels.DetallePedidoAlaboratorio.objects.filter(pedido=pedido)

            subtotal=0

            for detP in detallesPedido:
                lote=medmodels.Lote.objects.get(medicamento__pk=detP.medicamento.pk)
                detF=factmodels.DetalleFactura(
                    factura = factura,
                    cantidad = detP.cantidad,
                    medicamento = detP.medicamento,
                    precioUnitario = lote.precio,
                    importe = detP.cantidad * lote.precio
                )
                subtotal = subtotal + (detP.cantidad * lote.precio)
                listaDetallesFactura.append(detF)

            pieFactura = factmodels.pieDeFactura()
            pieFactura.factura = factura
            pieFactura.subtotal = subtotal
            pieFactura.iva = 21
            pieFactura.total = subtotal + 21

            #================esto debe hacerse de forma atomica===================
            form.save()#Guarda el encabezado.

            @transaction.atomic
            def guardarDetalle():
                for renglon in listaDetallesFactura:#Guarda los detalles (renglones).
                    factmodels.DetalleFactura.save(renglon)

            guardarDetalle()

            pieFactura.save()#Guarda el pie de pagina.
            pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedido)
            pedido.facturaAsociada = True
            pedido.save()
            #======================================================================

            erroresEnElForm = "FalseYsave"#Variable que establece que el form no tiene errores y que fue guardado en base.
        else:
            erroresEnElForm = "True"

        nroPedidoAlab=request.session['nroPedidoAlab']
    else:
        form = forms.RegistrarFactura()

    if request.method == "GET":

        valores=request.GET.items()
        if(valores):
            claveValor= valores[0]
            nroPedidoAlab=claveValor[1]
            request.session['nroPedidoAlab'] = nroPedidoAlab #Se guarda el numero de pediod de laboratorio en sesion


    filters = get_filtros_pedidos(request.GET, pmodels.PedidoAlaboratorio)
    claves = filters.keys()#Se obtiene las claves que vienen en el diccionario filtro

    if (len(claves)>1)and((claves[0]=="fecha__lte")or(claves[1]=="fecha__lte")):#Se verifica si vino un filtro y ademas si vienen fechas
            #El formato de facha dd/mm/yyyy hace que el render falle
            fecha1 = putils.formatearFecha(filters["fecha__lte"])#Esta funcion convierte de dd/mm/yyyy a yyyy-mm-dd
            fecha2 = putils.formatearFecha(filters["fecha__gte"])#para que funcione bien
            filters={'fecha__lte': fecha1, 'fecha__gte': fecha2}#Hay que reconstruir el diccionario con el formato nuevo

    listPedidos = pmodels.PedidoAlaboratorio.objects.filter(**filters).filter(estado="Completo",facturaAsociada=False)

    listLaboConPedCompleto=[]
    for laboConPedCompleto in listPedidos:
        listLaboConPedCompleto.append(laboConPedCompleto.laboratorio)

    estadisticas = {
        'total': listPedidos.count(),
        'filtrados': listPedidos.count()
    }

    return render(request,"Proveedores/facturacionCompras.html",{"listPedidos": listPedidos,"formFactura": form,"erroresEnElForm":erroresEnElForm,"nroPedidoAlab":nroPedidoAlab})










