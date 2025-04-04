from rest_framework import serializers
from .models import Entrada, Categoria
from cuenta.serializers import PerfilUsuarioSerializer


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = '__all__'

class EntradaSerializer(serializers.ModelSerializer):

    categoria = CategoriaSerializer(many=True)
    autor = PerfilUsuarioSerializer()

    class Meta:
        model = Entrada
        fields = '__all__'
        # fields = ['titulo', 'imagen', 'contenido', 'categoria', 'autor']