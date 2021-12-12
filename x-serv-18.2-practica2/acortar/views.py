from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template import loader
from urllib.parse import unquote

from .models import Contenido, Comentario


@csrf_exempt
def get_content(request, llave):
    try:
        url = Contenido.objects.filter(id=llave).get()
    except Contenido.DoesNotExist:
        return HttpResponseNotFound("Recurso no disponible")

    content = {'url': url}
    return render(request, 'acortar/redirect.html', content)


@csrf_exempt
def index(request):

    # --Recogemos la nueva url
    if request.method == "PUT":
        # --Nueva url
        url = request.body.decode('utf-8')

    elif request.method == "POST":
        action = request.POST['action']
        if action == "Enviar Contenido":
            url = request.POST['URL']

    if request.method == "GET":
        content_list = Contenido.objects.all()
        context = {'content_list': content_list}

        return render(request, 'acortar/index.html', context)

    elif request.method == "PUT" or request.method == "POST":
        if not url:
            return render(request, 'acortar/noContent.html')
        else:
            try:
                # --Vemos si esta ya dentro de la tabla
                c = Contenido.objects.get(clave=url)
            except Contenido.DoesNotExist:
                # --Creamos la url acortada.
                if (url[:4] != "http"):       # --No trae el http por delante
                    url = "http://" + url

                c = Contenido(clave=url)
                c.save()

            context = {'contenido': c}
            return render(request, 'acortar/content.html', context)
