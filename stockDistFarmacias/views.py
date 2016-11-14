from django.shortcuts import render
from stockDistFarmacias import models as distmodels
from pedidos import models as pmodels
from medicamentos import models as mmodels

def stockDistribuido(request):

    #mfilters = get_filtros(request.GET, models.PedidoDeFarmacia)
    #pedidos = models.PedidoDeFarmacia.objects.filter(**mfilters)

    distribuidos = mmodels.StockDistribuidoEnFarmacias.objects.all()

    #estadisticas = {
    #    'total': models.PedidoDeFarmacia.objects.all().count(),
    #    'filtrados': pedidos.count()
    #}
    return render(request, "stockDist.html", {"distribuidos": distribuidos})

