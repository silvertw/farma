
from django.shortcuts import render, redirect, get_object_or_404
import models, forms, time
from django.contrib.auth.decorators import login_required
from jsonview.decorators import json_view
from django.contrib.auth.decorators import permission_required
from easy_pdf.views import PDFTemplateView
from organizaciones.views import hubo_alta
from pedidos import models as pmodels
from pedidos import views as pviews
from django.db import transaction
from medicamentos import models as medmodels
import models as factmodels
import forms as factforms
from pedidos.views import get_filtros as get_filtros_pedidos
from pedidos import utils as putils
from django.http import HttpResponse
from django import utils
from xlsxwriter import Workbook
import io
import json

# Create your views here.

def facturacionVentas(request):

    if request.method == "GET":

        valores=request.GET.items()
        if(valores):
            claveValor= valores[0]
            nroPedidoAlab=claveValor[1]
            request.session['nroPedidoAlab'] = nroPedidoAlab #Se guarda el numero de pediod de laboratorio en sesion

    filters = get_filtros_pedidos(request.GET, pmodels.PedidoDeClinica)
    listPedidosClinicas = pmodels.PedidoDeClinica.objects.filter(**filters).filter(facturaAsociada=False)

    estadisticas = {
        'total': listPedidosClinicas.count(),
        'filtrados': listPedidosClinicas.count()
    }

    return render(request,"obSocialesYclinicas/facturacionVentas.html",{"listPedidosClinicas":listPedidosClinicas,"filtros": request.GET,"estadisticas":estadisticas})



def facturasEmitidas(request):

    filters = get_filtros_pedidos(request.GET, pmodels.PedidoDeClinica)
    listPedidosClinicas = pmodels.PedidoDeClinica.objects.filter(**filters).filter(facturaAsociada=True)

    estadisticas = {
          'total': listPedidosClinicas.count(),
          'filtrados': listPedidosClinicas.count(),
    }

    if "nroFactura" in request.GET:
        nroFacturaAbuscar= request.GET["nroFactura"]
        if nroFacturaAbuscar:
            try:
               facturaAclinica = factmodels.FacturaAclinica.objects.get(identificador=nroFacturaAbuscar)
               if facturaAclinica:
                   listPedidosClinicas=[]
                   pedidoDeClinica = facturaAclinica.pedidoRel
                   listPedidosClinicas.append(pedidoDeClinica)
                   estadisticas = {
                      'total': 1,
                      'filtrados': 1,
                   }
            except:
                listPedidosClinicas = []


    return render(request,"obSocialesYclinicas/facturasEmitidas.html",{"listPedidosClinicas":listPedidosClinicas,"filtros":request.GET,"estadisticas":estadisticas})

def registrarPagoDeFacturaVenta(request):
    if "nroPedido" in request.GET:
        nroPedidoPorGet=request.GET['nroPedido']

        facturaApagar=factmodels.FacturaAclinica.objects.get(pedidoRel=nroPedidoPorGet)
        facturaApagar.pagada=True
        facturaApagar.save()
        msj="El registro de pago se realizo correctamente"

        response = HttpResponse(msj)

    return response


@transaction.atomic
def emitirFactura(request):

    if "nroPedido" in request.GET:
        nroPedidoPorGet=request.GET["nroPedido"]
        pedidoClinica=pmodels.PedidoDeClinica.objects.get(nroPedido=nroPedidoPorGet)#Obtengo el pedido de clinica
        detallesPedidoClinica=pedidoClinica.get_detalles()#Obtengo el detalle del pedido
        facturaAclinica=factmodels.FacturaAclinica(

            tipo=1,
            fecha=time.strftime("%Y-%m-%d"),
            titular="Cosme",
            pedidoRel=pedidoClinica,
        )

        facturaAclinica.save()

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
        #================esto debe hacerse de forma atomica===================
        @transaction.atomic
        def guardarDetalle():
            for renglon in listaDetallesDeFacturaAclinica:#Guarda los detalles (renglones).
                factmodels.DetalleFacturaAclinica.save(renglon)
        guardarDetalle()
        pieFactura.save()#Guarda el pie de pagina.
        pedido = pmodels.PedidoDeClinica.objects.get(pk=nroPedidoPorGet)
        pedido.facturaAsociada = True
        pedido.save()
        #======================================================================

        msj="La Factura se Genero Correctamente"

        response = HttpResponse(msj)

    return response

#================================================IMPRESION DE FACTURA================================================
class imprimirFactura(PDFTemplateView):
    template_name = "obSocialesYclinicas/facturaCompras.html"

    def get_context_data(self, id):

        pedido=models.PedidoDeClinica.objects.get(pk=id)
        factura=models.FacturaAclinica.objects.get(pedidoRel=pedido)
        detaLLeFactura=models.DetalleFacturaAclinica.objects.filter(factura=factura)
        pieDeFactura=models.pieDeFacturaAclinica.objects.get(factura=factura)

        return super(imprimirFactura, self).get_context_data(
            pagesize="A4",
            factura=factura,
            detaLLeFactura=detaLLeFactura,
            pieDeFactura=pieDeFactura,
            pedido=pedido
        )
#================================================FIN IMPRESION DE FACTURA=============================================


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
                detF=factmodels.DetalleFacturaDeProveedor(
                    factura = factura,
                    cantidad = detP.cantidad,
                    medicamento = detP.medicamento,
                    precioUnitario = lote.precio,
                    importe = detP.cantidad * lote.precio
                )
                subtotal = subtotal + (detP.cantidad * lote.precio)
                listaDetallesFactura.append(detF)

            pieFactura = factmodels.pieDeFacturaDeProveedor()
            pieFactura.factura = factura
            pieFactura.subtotal = subtotal
            pieFactura.iva = 21
            pieFactura.total = subtotal + (subtotal*(21/100))

            #================esto debe hacerse de forma atomica===================
            form.save()#Guarda el encabezado.

            @transaction.atomic
            def guardarDetalle():
                for renglon in listaDetallesFactura:#Guarda los detalles (renglones).
                    factmodels.DetalleFacturaDeProveedor.save(renglon)

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

        if "idRow" in request.GET:
            nroPedidoAlab=request.GET["idRow"]
            request.session['nroPedidoAlab'] = nroPedidoAlab

    filters = get_filtros_pedidos(request.GET, pmodels.PedidoAlaboratorio)
    listPedidos = pmodels.PedidoAlaboratorio.objects.filter(**filters).filter(estado="Completo",facturaAsociada=False)

    listLaboConPedCompleto=[]
    for laboConPedCompleto in listPedidos:
        listLaboConPedCompleto.append(laboConPedCompleto.laboratorio)

    estadisticas = {
        'total': listPedidos.count(),
        'filtrados': listPedidos.count()
    }

    return render(request,"Proveedores/facturacionCompras.html",{"listPedidos": listPedidos,"formFactura": form,"erroresEnElForm":erroresEnElForm,"nroPedidoAlab":nroPedidoAlab,"filtros": request.GET,"estadisticas":estadisticas})



def facturasRegistradasCompras(request):

    if request.method == "POST":
        form = forms.Pago(request.POST)
        formEstadoDelPago=form.save(commit=False)
        nroPedidoAlab=request.session['nroPedidoAlab']
        pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedidoAlab)

        encabezadoFactura = factmodels.FacturaDeProveedor.objects.get(pedidoRel=pedido)
        encabezadoFactura.pagada=True
        encabezadoFactura.save()
        encabezadoFactura = factmodels.FacturaDeProveedor.objects.get(pedidoRel=pedido)

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
                encabezadoFactura = factmodels.FacturaDeProveedor.objects.get(pedidoRel=pedido)
                detalleFactura = factmodels.DetalleFacturaDeProveedor.objects.filter(factura=encabezadoFactura)
                pieDeFactura = factmodels.pieDeFacturaDeProveedor.objects.get(factura=encabezadoFactura)
                request.session['nroPedidoAlab'] = nroPedidoAlab
            else:
                encabezadoFactura=None
                detalleFactura=None
                pieDeFactura=None
                formEstadoDelPago=None
                nroPedidoAlab=None

    filters = get_filtros_pedidos(request.GET, pmodels.PedidoAlaboratorio)
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
            "filtros": request.GET,
            "estadisticas":estadisticas
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
            "filtros": request.GET,
            "estadisticas":estadisticas
        })


def factProveedEncabezadoModal(request):

    data=request.GET.items()
    claveValor=data[0]
    nroPedidoAlab=claveValor[1]
    #==========SE OBTIENE LA FACTURA DEL PEDIDO CON FACTURA REGISTRADA=================
    pedido = pmodels.PedidoAlaboratorio.objects.get(pk=nroPedidoAlab)
    encabezadoFactura = factmodels.FacturaDeProveedor.objects.get(pedidoRel=pedido)
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
    encabezadoFactura = factmodels.FacturaDeProveedor.objects.get(pedidoRel=pedido)
    detalleFactura = factmodels.DetalleFacturaDeProveedor.objects.filter(factura=encabezadoFactura)
    pieDeFactura = factmodels.pieDeFacturaDeProveedor.objects.get(factura=encabezadoFactura)
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
    encabezadoFactura = factmodels.FacturaDeProveedor.objects.get(pedidoRel=pedido)
    pieDeFactura = factmodels.pieDeFacturaDeProveedor.objects.get(factura=encabezadoFactura)
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
    encabezadoFactura = factmodels.FacturaDeProveedor.objects.get(pedidoRel=pedido)
    pieDeFactura = factmodels.pieDeFacturaDeProveedor.objects.get(factura=encabezadoFactura)
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
        encabezadoFactura = factmodels.FacturaDeProveedor.objects.get(pedidoRel=pedido)
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
    encabezadoFactura = factmodels.FacturaDeProveedor.objects.get(pedidoRel=pedido)
    encabezadoFactura.pagada=False
    encabezadoFactura.save()

    msj="El pago ha sido cancelado"
    response = HttpResponse(msj)

    return response



#=================================ESTADISTICAS FACTURACION PROVEEDORES==========================================
def estadisticasCompras(request):
    form = forms.RangoFechasForm(request.GET)
    estadistica = None
    if form.is_valid():
        estadistica = putils.estadisticasCompras(pviews.get_filtros, form.clean())
        request.session['estadistica'] = estadistica
    else:
        estadistica = request.session['estadistica']
    columnChart = estadistica['columnChart']
    pieChart = estadistica['pieChart']
    return render(request, "Proveedores/estadisticasCompras.html", {'columnChart':
            json.dumps(columnChart), 'pieChart': json.dumps(pieChart), 'form': form})

def estadisticasComprasExcel(request):
    datos = request.session['estadistica']['excel']
    excel = io.BytesIO()
    workbook = Workbook(excel, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    titulo = workbook.add_format({
        'font_name':'Arial',
        'font_size': 12,
        'font_color': 'navy',
        'bold': True
    })
    encabezado = workbook.add_format({
        'font_name':'Arial',
        'bold': True
    })
    alignLeft = workbook.add_format({
        'align':'left',
    })
    worksheet.write('A1:B1', 'Montos de Compras Realizas a Proveedores', titulo)

    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 20)
    worksheet.write('A2', '#', encabezado)
    worksheet.write('B2', 'Proveedor', encabezado)
    worksheet.write('C2', 'Monto', encabezado)
    fila = 2
    tope = len(datos)
    for i in range(0, tope):
        worksheet.write(fila, 0, i + 1, alignLeft)
        worksheet.write(fila, 1, datos[i]['proveedor'], alignLeft)
        worksheet.write(fila, 2, datos[i]['cantidad'], alignLeft)
        fila += 1
    workbook.close()

    excel.seek(0)

    response = HttpResponse(excel.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=estadisticasCompras.xlsx"
    return response



#=================================ESTADISTICAS FACTURACION VENTAS===============================================

def estadisticasVentas(request):
    form = forms.RangoFechasForm(request.GET)
    estadistica = None
    if form.is_valid():
        estadistica = putils.estadisticasVentas(pviews.get_filtros, form.clean())
        request.session['estadistica'] = estadistica
    else:
        estadistica = request.session['estadistica']
    columnChart = estadistica['columnChart']
    pieChart = estadistica['pieChart']
    return render(request, "obSocialesYclinicas/estadisticasVentas.html", {'columnChart':
            json.dumps(columnChart), 'pieChart': json.dumps(pieChart), 'form': form})



def estadisticasVentasExcel(request):
    datos = request.session['estadistica']['excel']
    excel = io.BytesIO()
    workbook = Workbook(excel, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    titulo = workbook.add_format({
        'font_name':'Arial',
        'font_size': 12,
        'font_color': 'navy',
        'bold': True
    })
    encabezado = workbook.add_format({
        'font_name':'Arial',
        'bold': True
    })
    alignLeft = workbook.add_format({
        'align':'left',
    })
    worksheet.write('A1:B1', 'Montos de Ventas Realizas a Clientes', titulo)

    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 20)
    worksheet.write('A2', '#', encabezado)
    worksheet.write('B2', 'Cliente', encabezado)
    worksheet.write('C2', 'Monto', encabezado)
    fila = 2
    tope = len(datos)
    for i in range(0, tope):
        worksheet.write(fila, 0, i + 1, alignLeft)
        worksheet.write(fila, 1, datos[i]['cliente'], alignLeft)
        worksheet.write(fila, 2, datos[i]['cantidad'], alignLeft)
        fila += 1
    workbook.close()

    excel.seek(0)

    response = HttpResponse(excel.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=estadisticasVentas.xlsx"
    return response
