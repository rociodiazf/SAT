from django import forms

from .models import Contenido, Comentario

class ContenidoForm(forms.ModelForm):

    class Meta:
        model = Contenido
        fields = ('clave', 'valor',)


class ContenidoForm_Comment(forms.ModelForm):

    class Meta:
        model = Comentario
        exclude = ['contenido', 'fecha']
