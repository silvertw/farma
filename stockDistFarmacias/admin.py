from django.contrib import admin
from medicamentos.models import StockFarmayFarmacias
from medicamentos.models import StockDistribuidoEnFarmacias
from django.contrib.auth import models as auth_models



admin.site.register(StockFarmayFarmacias)
admin.site.register(StockDistribuidoEnFarmacias)