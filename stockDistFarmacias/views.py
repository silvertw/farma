from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from stockDistFarmacias import models as distmodels
from pedidos import models as pmodels
from medicamentos import models as mmodels

def get_filtros(get, modelo):
    mfilter={}
    for filtro in modelo.FILTROS:
       if filtro in get and get[filtro]:
            attr = filtro
            value = get[filtro]

            if hasattr(modelo, "FILTERMAPPER") and filtro in modelo.FILTERMAPPER:
                attr = modelo.FILTERMAPPER[filtro]
                mfilter[attr] = value
    return mfilter


@permission_required('usuarios.encargado_general', login_url='login')
@permission_required('usuarios.encargado_stock', login_url='login')
@login_required(login_url='login')
def stockDistribuido(request):
    mfilters = get_filtros(request.GET, mmodels.StockDistribuidoEnFarmacias)
    distribuidos = mmodels.StockDistribuidoEnFarmacias.objects.filter(**mfilters).exclude(cantidad=0).order_by('farmacia','lote')
    estadisticas = {
        'total': mmodels.StockDistribuidoEnFarmacias.objects.exclude(cantidad=0).count(),
        'filtrados': distribuidos.count()
    }
    return render(request, "stockDist.html", {"distribuidos": distribuidos,"filtros": request.GET,"estadisticas":estadisticas})

