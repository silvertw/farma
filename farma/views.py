from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from minidetector import detect_mobile

def get_order(get):
    if "o" in get:
        return get["o"]


@login_required(login_url='login')
def inicio(request):
    if request.mobile:
        #vista movil
        return render(request, "mobile/inicio_mobile.html")
    else:
        #vista pc
        return render(request, "inicio/inicio.html")


def paginaEnConstruccion(request):
    return render(request, "paginaEnConstruccion.html")