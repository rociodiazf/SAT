from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template import loader
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Contenido, Comentario


@csrf_exempt
def get_content(request, llave):
    if request.method == "PUT":
        valor = request.body.decode('utf-8')
    elif request.method == "POST":
        action = request.POST['action']
        if action == "Enviar Contenido":
            valor = request.POST['valor']
    if request.method == "PUT" or (request.method == "POST" and action == "Enviar Contenido"):
        try:
            c = Contenido.objects.get(clave=llave)
            c.valor = valor
        except Contenido.DoesNotExist:
            c = Contenido(clave=llave, valor=valor)
        c.save()
    if request.method == "POST" and action == "Enviar Comentario":
            c = get_object_or_404(Contenido, clave=llave)
            titulo = request.POST['titulo']
            cuerpo = request.POST['cuerpo']
            q = Comentario(contenido=c, titulo=titulo, cuerpo=cuerpo, fecha=timezone.now())
            q.save()

    contenido = get_object_or_404(Contenido, clave=llave)
    context = {'contenido': contenido}
    return render(request, 'cms/content.html', context)

def index(request):
    content_list = Contenido.objects.all()[:5]
    context = {'content_list': content_list}
    return render(request, 'cms/index.html', context)

def loggedIn(request):
    if request.user.is_authenticated:
        logged = "Logged in as " + request.user.username
    else:
        logged = "Not logged in. <a href='/admin/'>Login via admin</a>"
    return HttpResponse(logged)

def logout_view(request):
    logout(request)
    return redirect("/cms/")

def imagen(request):
    template = loader.get_template('cms/plantilla.html')
    context = {}
    return HttpResponse(template.render(context, request))
