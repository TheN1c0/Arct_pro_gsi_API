from rest_framework import serializers
from .models import Categoria, Pedido

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']  # Especificamos los campos que queremos incluir


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'  # Incluye todos los campos del modelo Pedido
