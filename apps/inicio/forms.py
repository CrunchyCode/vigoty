from django import forms
from django.contrib.auth.models import User
from .models import Perfil


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('direccion', 'telefono', 'documento_identidad')
