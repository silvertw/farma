from django.shortcuts import render
from stockDistFarmacias import models as distmodels
from pedidos import models as pmodels
from medicamentos import models as mmodels

def get_filtros(get, modelo):
    mfilter = {}
    for filtro in modelo.FILTROS:
        attr = filtro.split("__")[0]
        if attr in get and get[attr]:
            mfilter[filtro] = get[attr]
            mfilter[attr] = get[attr]
    return mfilter

def stockDistribuido(request):

    filters = get_filtros(request.GET, mmodels.StockDistribuidoEnFarmacias)
    mfilters = dict(filter(lambda v: v[0] in mmodels.StockDistribuidoEnFarmacias.FILTROS, filters.items()))
    distribuidos = mmodels.StockDistribuidoEnFarmacias.objects.filter(**mfilters)

    estadisticas = {
        'total': mmodels.StockDistribuidoEnFarmacias.objects.all().count(),
        'filtrados': distribuidos.count()
    }

    return render(request, "stockDist.html", {"distribuidos": distribuidos,"filtros": filters})

