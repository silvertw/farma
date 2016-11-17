
from django.shortcuts import render, redirect, get_object_or_404
import models, forms, time
from django.contrib.auth.decorators import login_required
from jsonview.decorators import json_view
from django.contrib.auth.decorators import permission_required
from easy_pdf.views import PDFTemplateView
from organizaciones.views import hubo_alta
from pedidos import models as pmodels
from django.db import transaction
from medicamentos import models as medmodels
import models as factmodels
import forms as factforms
from pedidos.views import get_filtros as get_filtros_pedidos
from pedidos import utils as putils
from django.http import HttpResponse
from django import utils
import json

# Create your views here.

def facturacionVentas(request):

    #if request.method == "GET":

    #    valores=request.GET.items()
    #    if(valores):
    #        claveValor= valores[0]
    #        nroPedidoAlab=claveValor[1]
    #        request.session['nroPedidoAlab'] = nroPedidoAlab #Se guarda el numero de pediod de laboratorio en sesion

    filters = get_filtros_pedidos(request.GET, pmodels.PedidoDeClinica)
    claves = filters.keys()#Se obtiene las claves que vienen en el diccionario filtro

    if (len(claves)>1)and((claves[0]=="fecha__lte")or(claves[1]=="fecha__lte")):#Se verifica si vino un filtro y ademas si vienen fechas
            #El formato de facha dd/mm/yyyy hace que el render falle
            fecha1 = putils.formatearFecha(filters["fecha__lte"])#Esta funcion convierte de dd/mm/yyyy a yyyy-mm-dd
            fecha2 = putils.formatearFecha(filters["fecha__gte"])#para que funcione bien
            filters={'fecha__lte': fecha1, 'fecha__gte': fecha2}#Hay que reconstruir el diccionario con el formato nuevo

    listPedidosClinicas = pmodels.PedidoDeClinica.objects.filter(**filters).filter(facturaAsociada=False)

    estadisticas = {
        'total': listPedidosClinicas.count(),
        'filtrados': listPedidosClinicas.count()
    }

    return render(request,"obSocialesYclinicas/facturacionVentas.html",{"listPedidosClinicas":listPedidosClinicas})

@transaction.atomic
def emitirFactura(request):

    valores=request.GET.items()
    if(valores):
        claveValor= valores[0]
        nroPedidoPorGet=claveValor[1]

        pedidoClinica=pmodels.PedidoDeClinica.objects.get(nroPedido=nroPedidoPorGet)#Obtengo el pedido de clinica
        detallesPedidoClinica=pedidoClinica.get_detalles()#Obtengo el detalle del pedido

        facturaAclinica=factmodels.FacturaAclinica(

            tipo=1,
            identificador="1",
            fecha=time.strftime("%Y-%m-%d"),
            titular="Cosme",
            pedidoRel=pedidoClinica,
        )

        print "identi",facturaAclinica.identificador
        print "fecha", facturaAclinica.fecha
        print "titular", facturaAclinica.titular
        print "pedido",facturaAclinica.pedidoRel

        listaDetallesDeFacturaAclinica=[]
        subtotal=0
        for detP in detallesPedidoClinica:
            lotes=medmodels.Lote.objects.filter(medicamento__pk=detP.medicamento.pk)
            lote=lotes[0]

            detF=factmodels.DetalleFacturaAclinica(
                factura = facturaAclinica,
                cantidad = detP.cantidad,
                medicamento = detP.medicamento,
                precioUnitario = lote.precio,
                importe = detP.cantidad * lote.precio
            )
            subtotal = subtotal + (detP.cantidad * lote.precio)
            listaDetallesDeFacturaAclinica.append(detF)

        pieFactura = factmodels.pieDeFacturaAclinica()
        pieFactura.factura = facturaAclinica
        pieFactura.subtotal = subtotal
        pieFactura.iva = 21
        pieFactura.total = subtotal + (subtotal*(21/100))

        facturaAclinica.save()
        #================esto debe hacerse de forma atomica===================
        @transaction.atomic
        def guardarDetalle():
            for renglon in listaDetallesDeFacturaAclinica:#Guarda los detalles (renglones).
                factmodels.DetalleFacturaAclinica.save(renglon)
        guardarDetalle()
        pieFactura.save()#Guarda el pie de pagina.
        pedido = pmodels.PedidoDeClinica.objects.get(pk=nroPedidoPorGet)
        pedido.facturaAsociada = True
        #======================================================================

    msj="La Factura se Genero Correctamente"
    response = HttpResponse(msj)

    return response

#================================================IMPRESION DE FACTURA================================================
#class remitoOptimizarStock(PDFTemplateView):
#    template_name = "obSocialesYclinicas/facturaCompras.html"

#    def get_context_data(self, id):

#        movimiento=models.movimientosDeStockDistribuido.objects.get(pedidoMov__pk=id)
#        pedido=models.PedidoDeFarmacia.objects.get(pk=id)
#        actividadMovimiento=movimiento.movimiento


#        return super(remitoOptimizarStock, self).get_context_data(
#            pagesize="A4",
            #remito=pedido,
            #detallesRemito=renglones
#        )
#================================================FIN IMPRESION DE FACTURA=============================================










def facturasEmitidas(request):

    return render(request,"obSocialesYclinicas/facturasEmitidas.html",{})





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

            factura.pedidoRel=pedido#Se setea el pedido asocioado a esta factura

            subtotal=0

            for detP in detallesPedido:
                lotes=medmodels.Lote.objects.filter(medicamento__pk=detP.medicamento.pk)
                lote=lotes[0]
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
            pieFactura.total = subtotal + (subtotal*(21/100))

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



def facturasRegistradasCompras(request):

    if request.method == "POST":
        form = forms.Pago(request.POST)
        formEstadoDelPago=form.save(commit=False)
        nroPedidoAlab=request.session['nroPedidoAlab']
        pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedidoAlab)

        encabezadoFactura = factmodels.Factura.objects.get(pedidoRel=pedido)
        encabezadoFactura.pagada=True
        encabezadoFactura.save()
        encabezadoFactura = factmodels.Factura.objects.get(pedidoRel=pedido)

        formEstadoDelPago.factura=encabezadoFactura
        formEstadoDelPago.save()
    else:
        formEstadoDelPago = forms.Pago()
        data=request.GET.items()#SE OBTIENEN LOS ITEMS DEL GET
        if data:#SI VINIERON DATOS
            claveValor=data[0]#SE OBTIENE LA CLAVE
            if claveValor[0]=='idRowVer':
                nroPedidoAlab=claveValor[1]
                #==========SE OBTIENE LA FACTURA DEL PEDIDO CON FACTURA REGISTRADA=================
                pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedidoAlab)
                encabezadoFactura = factmodels.Factura.objects.get(pedidoRel=pedido)
                detalleFactura = factmodels.DetalleFactura.objects.filter(factura=encabezadoFactura)
                pieDeFactura = factmodels.pieDeFactura.objects.get(factura=encabezadoFactura)
                request.session['nroPedidoAlab'] = nroPedidoAlab
            else:
                encabezadoFactura=None
                detalleFactura=None
                pieDeFactura=None
                formEstadoDelPago=None
                nroPedidoAlab=None

    filters = get_filtros_pedidos(request.GET, pmodels.PedidoAlaboratorio)
    filters2 = get_filtros_pedidos(request.GET, factmodels.Factura)

    claves = filters.keys()#Se obtiene las claves que vienen en el diccionario filtro

    if (len(claves)>1)and((claves[0]=="fecha__lte")or(claves[1]=="fecha__lte")):#Se verifica si vino un filtro y ademas si vienen fechas
            #El formato de facha dd/mm/yyyy hace que el render falle
            fecha1 = putils.formatearFecha(filters["fecha__lte"])#Esta funcion convierte de dd/mm/yyyy a yyyy-mm-dd
            fecha2 = putils.formatearFecha(filters["fecha__gte"])#para que funcione bien
            filters={'fecha__lte': fecha1, 'fecha__gte': fecha2}#Hay que reconstruir el diccionario con el formato nuevo

    listPedidos = pmodels.PedidoAlaboratorio.objects.filter(**filters).filter(estado="Completo",facturaAsociada=True)

    listLaboConPedCompleto=[]
    for laboConPedCompleto in listPedidos:
        listLaboConPedCompleto.append(laboConPedCompleto.laboratorio)

    estadisticas = {
        'total': listPedidos.count(),
        'filtrados': listPedidos.count()
    }

    if request.GET.items():#Si get tiene valores se debe devolver la factura
        return render(request,"Proveedores/facturasRegistradasDeCompras.html",{
            "listPedidos": listPedidos,
            "encabezadoFactura":encabezadoFactura,
            "detalleFactura":detalleFactura,
            "pieDeFactura":pieDeFactura,
            "formEstadoDelPago":formEstadoDelPago,
            "nroPedidoAlab":nroPedidoAlab,
        })
    else:
        encabezadoFactura=None
        detalleFactura=None
        pieDeFactura=None
        formEstadoDelPago=None
        nroPedidoAlab=None
        return render(request,"Proveedores/facturasRegistradasDeCompras.html",{
            "listPedidos": listPedidos,
            "encabezadoFactura":encabezadoFactura,
            "detalleFactura":detalleFactura,
            "pieDeFactura":pieDeFactura,
            "formEstadoDelPago":formEstadoDelPago,
            "nroPedidoAlab":nroPedidoAlab,
        })


def factProveedEncabezadoModal(request):

    data=request.GET.items()
    claveValor=data[0]
    nroPedidoAlab=claveValor[1]
    #==========SE OBTIENE LA FACTURA DEL PEDIDO CON FACTURA REGISTRADA=================
    pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedidoAlab)
    encabezadoFactura = factmodels.Factura.objects.get(pedidoRel=pedido)
    pago="false"
    request.session['nroPedidoAlab'] = nroPedidoAlab

    if encabezadoFactura.pagada:
        pago="true"
    return render(request, "Proveedores/_factProveedEncabezadoModal.html", {
        "encabezadoFactura":encabezadoFactura,
        "nroPedidoAlab":nroPedidoAlab,
        "pago":pago,
    })

def factProveedDetalleModal(request):

    data=request.GET.items()
    claveValor=data[0]
    nroPedidoAlab=claveValor[1]

    #==========SE OBTIENE LA FACTURA DEL PEDIDO CON FACTURA REGISTRADA=================
    pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedidoAlab)
    encabezadoFactura = factmodels.Factura.objects.get(pedidoRel=pedido)
    detalleFactura = factmodels.DetalleFactura.objects.filter(factura=encabezadoFactura)
    pieDeFactura = factmodels.pieDeFactura.objects.get(factura=encabezadoFactura)
    request.session['nroPedidoAlab'] = nroPedidoAlab

    return render(request, "Proveedores/_factProveedDetalleModal.html", {
        "encabezadoFactura":encabezadoFactura,
        "detalleFactura":detalleFactura,
        "nroPedidoAlab":nroPedidoAlab,
        "pieDeFactura":pieDeFactura,
    })

def factProveedFooterModal(request):

    data=request.GET.items()
    claveValor=data[0]
    nroPedidoAlab=claveValor[1]
    #==========SE OBTIENE LA FACTURA DEL PEDIDO CON FACTURA REGISTRADA=================
    pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedidoAlab)
    encabezadoFactura = factmodels.Factura.objects.get(pedidoRel=pedido)
    pieDeFactura = factmodels.pieDeFactura.objects.get(factura=encabezadoFactura)
    request.session['nroPedidoAlab'] = nroPedidoAlab

    return render(request, "Proveedores/_factProveedFooterModal.html",{
        "pieDeFactura":pieDeFactura,
        "nroPedidoAlab":nroPedidoAlab,
    })

def formularioDePago(request):
    #no hay forma que no entre por get y con datos
    formEstadoDelPago = forms.Pago()
    data=request.GET.items()
    claveValor=data[0]
    nroPedidoAlab=claveValor[1]
    pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedidoAlab)
    encabezadoFactura = factmodels.Factura.objects.get(pedidoRel=pedido)
    pieDeFactura = factmodels.pieDeFactura.objects.get(factura=encabezadoFactura)
    request.session['nroPedidoAlab'] = nroPedidoAlab

    return render(request, "Proveedores/_formularioDePago.html", {
        "formEstadoDelPago":formEstadoDelPago,
        "pieDeFactura":pieDeFactura,
        "encabezadoFactura":encabezadoFactura,
    })


def mostrarPago(request):

    data=request.GET.items()
    if data:
        claveValor=data[0]
        nroPedidoAlab=claveValor[1]
        #==========SE OBTIENE LA FACTURA DEL PEDIDO CON FACTURA REGISTRADA=================
        pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedidoAlab)
        encabezadoFactura = factmodels.Factura.objects.get(pedidoRel=pedido)
        request.session['nroPedidoAlab'] = nroPedidoAlab
        if encabezadoFactura.pagada:
            listaDePagos=factmodels.Pago.objects.filter(factura=encabezadoFactura)#recupera datos sobre el pago de factura
            ultimo=len(listaDePagos)#Se deja un historial de pagos que fueron cancelados para rehacer
                                    #o dejar cancelados indefinidamente.
            pagoRec=listaDePagos[ultimo-1]
            if (ultimo>1):
                listaCancelados=listaDePagos
            else:
                listaCancelados=None

        else:
            pagoRec=None
    return render(request, "Proveedores/_mostrarPago.html", {"pagoRec":pagoRec,"listaCancelados":listaCancelados,"ultimo":ultimo})


def formaDePago_add(request):
    if request.method == "POST":
        form = forms.formaDePago(request.POST)
        if form.is_valid():
            form.save()
            if '_volver' in request.POST:
                return redirect('formaDePago_add')
            else:
                request.session['successAdd'] = True
                return redirect('formaDePago_add')
    else:
        form = forms.formaDePago()
    successAdd = hubo_alta(request.session)
    return render(request, "FormasDePago/FormasDePago_add.html", {"form": form, 'successAdd': successAdd})

def cancelarPago(request):
    data=request.GET.items()
    claveValor=data[0]
    nroPedidoAlab=claveValor[1]
    pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedidoAlab)
    encabezadoFactura = factmodels.Factura.objects.get(pedidoRel=pedido)
    encabezadoFactura.pagada=False
    encabezadoFactura.save()

    msj="El pago ha sido cancelado"
    response = HttpResponse(msj)

    return response