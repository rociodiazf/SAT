from django.shortcuts import render, get_object_or_404
from urllib.request import urlopen
from .ytchannel import YTChannel
from .redditnews import RedditNews
from .models import Alimentador, Item, Comentario, Vote
from .forms import UsersForm, PhotoForm,CommentForm
from django.shortcuts import redirect
from django.contrib.auth import logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.utils import timezone

def puntuacion_alim ():
    for alim in Alimentador.objects.all():
        Up = 0
        Down = 0
        for item in alim.item_set.all():
            for voto in item.vote_set.all():
                if voto.thumbsUp:
                    Up = Up +1
                elif voto.thumbsDown:
                    Down = Down +1
        alim.puntuacion = Up - Down
        alim.save()
    alimentadores = Alimentador.objects.order_by('-puntuacion')
    return alimentadores

def puntuacion_item ():
    for item in Item.objects.all():
        # __init__
        item.votos_positivos = 0
        item.votos_negativos = 0
        item.puntuacion = 0

        for voto in item.vote_set.all():
            if voto.thumbsUp:
                item.votos_positivos = item.votos_positivos +1
            elif voto.thumbsDown:
                item.votos_negativos = item.votos_negativos +1
        item.puntuacion = (item.votos_positivos - item.votos_negativos)
        item.save()
    #ordenamos el diccionario
    item_list = Item.objects.order_by('-puntuacion')

    return item_list

def parseYoutube(index):
    xmlStream = urlopen('https://www.youtube.com/feeds/videos.xml?channel_id=' + index)
    link = ('https://www.youtube.com/channel/' + index)
    channel = YTChannel(xmlStream)
    # Comprobamos si ya existe el alimentador
    try:
        alimentador = Alimentador.objects.get(link=channel.uriAlim())
    except Alimentador.DoesNotExist:
        alimentador = Alimentador(name= channel.nameAlim(),
                      link=channel.uriAlim(), id = index)
        alimentador.save()
    # Igualmente actualizamos
    for video in channel.videos():
        video = Item(alimentador = alimentador, title=video['title'],
                      link=video['link'], description = video['description'], id = video['id'])
        video.save()

def parseReddit(index):
    xmlStream = urlopen('https://www.reddit.com/r/' + index + '.rss')
    link = ('https://www.reddit.com/r/' + index )
    subreddit = RedditNews(xmlStream)
    # Comprobamos si ya existe el alimentador
    try:
        alimentador = Alimentador.objects.get(name = subreddit.nameAlim())
    except Alimentador.DoesNotExist:
        alimentador = Alimentador(name= subreddit.nameAlim(),
                      link=subreddit.uriAlim(), id = index)
        alimentador.save()
    # Igualmente actualizamos
    for new in subreddit.news():
        new = Item(alimentador = alimentador, title=new['title'],
                      link=new['link'], description = new['description'], id = new['id'])
        new.save()



def index(request):
    if request.method == "POST":
        # ¿De que alimentados procede?
        action = request.POST['action']
        # YOUTUBE
        if action == "Enseñame el canal":
            id = request.POST['valor']
            if not id or id[0] == " ":
                return render(request, 'miscosas/noContent.html')
            else:
                parseYoutube(id)

        elif action == "Dame las noticias":
            name = request.POST['valor']

            if not name or name[0] == " ":
                return render(request, 'miscosas/noContent.html')
            else:
                parseReddit(name)

        elif action == "Eliminar":
            alim_id = request.POST['alim_id']
            alimentador = Alimentador.objects.get(id = alim_id)
            alimentador.selected = False
            alimentador.save()
            return redirect('/miscosas/')

        elif action == "Selecionar":
            alim_id = request.POST['alim_id']
            alimentador = Alimentador.objects.get(id = alim_id)
            # Es youtbe o es reddit
            if alimentador.link[12:19] == "youtube":
                parseYoutube(alimentador.id)
            else:
                parseReddit(alimentador.id)

        alimentadores_list = Alimentador.objects.all()
        context = {'alimentadores_list': alimentadores_list}
        return redirect('/miscosas/alimentadores')
    elif request.method == "GET":
        # puntuacion de los items
        item_list = puntuacion_item()
        # alimentadores
        alimentadores_list = puntuacion_alim ()  # actualizamos las puntuaciones
        votes = None
        if request.user.is_authenticated:
            try:
                votes = request.user.vote_set.order_by('id')
                votes = request.user.vote_set.all()[:6]

            except Vote.DoesNotExist:
                votes = None
        context = {'item_list': item_list[:10],'alimentadores_list': alimentadores_list,'votes':votes}
        # puntuacion de los alimentadores
        return render(request, 'miscosas/index.html', context)

def alimentadores(request):
    alimentadores_list = Alimentador.objects.all()
    alimentadores_list = puntuacion_alim ()  # actualizamos las puntuaciones
    context = {'alimentadores_list': alimentadores_list}
    return render(request, 'miscosas/alimentadores.html', context)

def alimentador_info(request, alim_id):
    if request.method == "GET":
        try:
            alimentador = Alimentador.objects.get(id = alim_id)
        except Alimentador.DoesNotExist:
            return render(request, 'miscosas/noContent.html')
        context = {'alimentador': alimentador}
        return render(request, 'miscosas/alimentador_info.html', context)
    elif request.method == "POST":
        action = request.POST['select']
        alim_id = request.POST['alim_id']
        alimentador = Alimentador.objects.get(id = alim_id)
        if action == "Deseleccionar":
            alimentador.selected = False
        elif action == "Seleccionar":
            alimentador.selected = True
        alimentador.save()
        return redirect(request.path)



def item(request, item_id):
    if request.method == "GET":
        item = Item.objects.get(id = item_id)
        # Es youtbe o es reddit
        alim = item.alimentador.link[12:19] == "youtube"
        voto = None
        if request.user.is_authenticated:
            try:
                voto = Vote.objects.get(item = item, user = request.user)
            except Vote.DoesNotExist:
                voto = Vote(user= request.user,
                              item=item)
                voto.save()
        context = {'item': item, 'alim': alim, 'voto': voto}
        return render(request, 'miscosas/item_info.html', context)

    elif request.method == "POST":
        item_id = request.POST['item_id']
        item = get_object_or_404(Item, id = item_id)
        voto = get_object_or_404(Vote, item = item, user = request.user)

        action = request.POST['thumbs']
        if action == "Up" and voto.thumbsDown:
            voto.thumbsDown = False
            voto.thumbsUp = True
        elif action == "Down" and voto.thumbsUp:
            voto.thumbsDown = True
            voto.thumbsUp = False
        elif not (voto.thumbsDown and voto.thumbsUp):
            if action == "Up":
                voto.thumbsUp = True
            elif action == "Down":
                voto.thumbsDown = True
        voto.save()
        # recuento de votos
        puntuacion_item()
        # alimentadores
        puntuacion_alim ()  # actualizamos las puntuaciones
        return redirect(request.path)
    return(request.path)


def users(request):
    users_list = User.objects.all()
    context = {'users_list': users_list}
    return render(request, 'miscosas/users.html', context)

def user_info(request, user_id):
    user = User.objects.get(username = user_id)

    context = {'usuario': user,}
    return render(request, 'miscosas/user.html', context)

def new_user(request):
    if request.method == "POST":
        form = UsersForm(request.POST)
        if form.is_valid():
            user = form.save()
            do_login(request, user)
            return redirect('/miscosas/user/' + user.username)
    else:
        form = UsersForm()
    return render(request, 'miscosas/new_user.html', {'form': form})

def profilePhoto(request, user_name):
    if request.method == "POST":
        user = User.objects.get(username = user_name)
        form = PhotoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/miscosas')

    else:
        form = PhotoForm()
    return render(request, 'miscosas/new_user.html', {'form': form})

def loggedIn(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data =request.POST)

        # Recuperamos las credenciales validadas
        username = request.POST['username']
        password = request.POST['password']
        # Verificamos las credenciales del usuario
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return render(request, "miscosas/login.html", {'form': form})

        # Si existe un usuario con ese nombre y contraseña
        if user is not None:
            # Hacemos el login manualmente
            do_login(request, user)
            # Y le redireccionamos a la portada
            return redirect('/miscosas')

    # Si llegamos al final renderizamos el formulario
    return render(request, "miscosas/login.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect("/miscosas/")
def info(request):
    return render(request, 'miscosas/info.html')

def item_comment(request, item_id):
    item = get_object_or_404(Item, id = item_id)
    if request.method == "POST":
        user = request.user
        comment = Comentario(item = item, user = user, fecha=timezone.now())
        form = CommentForm(request.POST, instance = comment)

        if form.is_valid():
            comentario = form.save()
            return redirect('item_info', item_id=item_id)
    else:
        form = CommentForm()
    return render(request, 'miscosas/new_comment.html', {'form': form, 'item':item})
