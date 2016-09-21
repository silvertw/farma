
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.

def facturacionVentas(request):

    return render(request,"ClinicasYobrasSociales/facturacionVentas.html",{})

def facturacionCompras(request):

    return render(request,"Proveedores/facturacionCompras.html",{})

