from django.db import models


class Contenido(models.Model):
    clave = models.CharField(max_length=64)  # --Url

    # --El Id podriva ser la url acortada ya que es un numero secuencial.
    def __str__(self):
        return self.clave


class Comentario(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    cuerpo = models.TextField(blank=False)
    fecha = models.DateTimeField('publicado')

    def __str__(self):
        return self.titulo
