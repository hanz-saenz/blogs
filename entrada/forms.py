from django import forms
from .models import Entrada, Categoria

class EntradaForm(forms.ModelForm):

    class Meta:
        model = Entrada
        fields = ['titulo', 'imagen', 'contenido', 'categoria', 'autor']


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['nombre']