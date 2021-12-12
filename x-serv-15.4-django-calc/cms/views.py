from django.shortcuts import render

from django.http import HttpResponse
from .models import Contenido

def get_content(request, llave):
    try:
        respuesta = Contenido.objects.get(clave=llave).valor
    except Contenido.DoesNotExist:
        respuesta = 'No existe contenido para la clave ' + llave
    return HttpResponse(respuesta)
