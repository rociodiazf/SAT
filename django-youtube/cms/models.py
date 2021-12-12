from django.db import models

class Selecionados(models.Model):
    video = models.CharField(max_length=100)

    def __str__(self):
        return self.video


class Selecionables(models.Model):
    video = models.CharField(max_length=100)

    def __str__(self):
        return self.video
