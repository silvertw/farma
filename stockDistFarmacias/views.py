from django.shortcuts import render
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
    print "-->",mfilter
    return mfilter


def stockDistribuido(request):

    mfilters = get_filtros(request.GET, mmodels.StockDistribuidoEnFarmacias)
    #mfilters={'lote__medicamento':'ibu4'}
    distribuidos = mmodels.StockDistribuidoEnFarmacias.objects.filter(**mfilters)

    estadisticas = {
        'total': mmodels.StockDistribuidoEnFarmacias.objects.all().count(),
        'filtrados': distribuidos.count()
    }

    return render(request, "stockDist.html", {"distribuidos": distribuidos,"filtros": request.GET})

