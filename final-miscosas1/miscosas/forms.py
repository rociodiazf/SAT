from django import forms
from django.contrib.auth.models import User
from .models import ProfilePhoto, Comentario

class UsersForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','email', 'password',)


class PhotoForm(forms.ModelForm):

    class Meta:
        model = ProfilePhoto
        fields = ('foto_perfil',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comentario
        exclude = ['user', 'item', 'fecha']
