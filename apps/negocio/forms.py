from django import forms
from .models import Plato, Menu


class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ('nombre', 'ingredientes', 'tipo_plato', 'imagen')


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = (
            'cantidad_maxima', 'nombre', 'breve_descripcion',
            'precio', 'tipo_entrega'
        )
