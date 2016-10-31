#limpiador de sesion
def limpiar_sesion(lista, session):
    for item in lista:
        if item in session:
            del session[item]


#en la view
def pedidoDeFarmacia_add(request):
    limpiar_sesion(["pedidoDeFarmacia", "detallesPedidoDeFarmacia"], request.session)#limpia la sesion con limpiador de sesion
    if request.method == "POST":
        form = forms.PedidoDeFarmaciaForm(request.POST)#recupera el form que viene por post
        if form.is_valid():#verifica si es valido
            pedido = form.save(commit=False)#guarda en la variable pedido (no persiste en base)
            request.session['pedidoDeFarmacia'] = utils.crear_pedido_para_sesion(models.PedidoDeFarmacia, pedido)#guarda el edido en la sesion
            return redirect('detallesPedidoDeFarmacia')#redirige a la vista indicada
    else:
            form = forms.PedidoDeFarmaciaForm()
    return render(request, "pedidoDeFarmacia/pedidoAdd.html", {"form": form})


def detallesPedidoDeFarmacia(request):
    detalles = request.session.setdefault("detallesPedidoDeFarmacia", [])#crea en sesion un detalle de pedido vacio
    pedido = request.session['pedidoDeFarmacia']#recupera el pedido que habia guardado en la sesion
    #Devuelve el pedido y el detalle de pedido al template para que se comienze a cargar items
    return render(request, "pedidoDeFarmacia/detallesPedido.html", {'pedido': pedido, 'detalles': detalles}) 


#con esta view se agregan detalles (items) al pedido de farmacia
def detallePedidoDeFarmacia_add(request):
    success = True
    form = forms.DetallePedidoDeFarmaciaForm(request.POST or None)#recupera el formulario de detalles de pedido
    if request.method == 'POST':
        if form.is_valid():#si los datos son correctos
            det = form.save(commit=False)#guarda el form en la variable det pero no en la base
            detalles = request.session['detallesPedidoDeFarmacia']#recupera la lista vacia que se creo en la sesion en la view anterior
            
            #se fija si estoy tratando de poner 2 veces el mismo medicamento en el detalle	
            if not utils.existe_medicamento_en_pedido(detalles, det.medicamento.id):
                detalles.append(utils.crear_detalle_json(det, len(detalles) + 1))#si no es asi agrega el item pero convertido a json por que esta trabajando en sesion
                request.session['detallesPedidoDeFarmacia'] = detalles#cada vez que agrega un detalle actualiza o pisa en la sesion
                form = forms.DetallePedidoDeFarmaciaForm()#recupera el form nuevamente .
                form_html = render_crispy_form(form, context=update_csrf(request))#aca nose que hace.
                return {'success': success, 'form_html': form_html, 'detalles': detalles}
            else:  # medicamento ya existe en el pedido
                return {'success': False}
        else:
            success = False
    form_html = render_crispy_form(form, context=update_csrf(request))
    return {'success': success, 'form_html': form_html}








#una vez que damos registrar en este template el evento click de dicho boton nos lleva a la siguiente vista

def pedidoDeFarmacia_registrar(request):
    pedido = request.session['pedidoDeFarmacia']
    detalles = request.session['detallesPedidoDeFarmacia']
    mensaje_error = None
    if detalles:
        farmacia = omodels.Farmacia.objects.get(pk=pedido['farmacia']['id'])
        fecha = datetime.datetime.strptime(pedido['fecha'], '%d/%m/%Y').date()
        if not(models.PedidoDeFarmacia.objects.filter(pk=pedido["nroPedido"]).exists()):
            p = models.PedidoDeFarmacia(farmacia=farmacia, fecha=fecha)
            p.save()
            for detalle in detalles:
                medicamento = mmodels.Medicamento.objects.get(pk=detalle['medicamento']['id'])
                d = models.DetallePedidoDeFarmacia(pedidoDeFarmacia=p, medicamento=medicamento, cantidad=detalle['cantidad'])
                d.save()
            utils.procesar_pedido_de_farmacia(p)
            existeRemito = p.estado != "Pendiente"
            if existeRemito:
                nroRemito = models.RemitoDeFarmacia.objects.get(pedidoFarmacia__pk=p.pk)
                return {'success': True, 'existeRemito': True, 'nroRemito': nroRemito.id}
            else:
                return {'success': True, 'existeRemito': False}
        else:
            mensaje_error = "El pedido ya Existe!"
    else:
        mensaje_error = "No se puede registrar un pedido sin detalles"
    return {'success': False, 'mensaje-error': mensaje_error}               


