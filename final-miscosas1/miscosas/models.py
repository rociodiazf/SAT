from django.db import models
from django.contrib.auth.models import User

class Alimentador(models.Model):
    name = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    id = models.CharField(max_length=256, primary_key = True)
    selected = models.BooleanField(default=True)
    puntuacion = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.link

class Item(models.Model):
    alimentador = models.ForeignKey(Alimentador, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    id = models.CharField(max_length=256, primary_key = True)
    puntuacion = models.IntegerField(blank=True, null=True)
    votos_positivos = models.IntegerField(blank=True, null=True)
    votos_negativos = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.link


class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    cuerpo = models.TextField(blank=False)
    fecha = models.DateTimeField('publicado')

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    thumbsUp = models.BooleanField(default=False)
    thumbsDown = models.BooleanField(default=False)

class ProfilePhoto (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='miscosas/media/', blank=True, null=True)
