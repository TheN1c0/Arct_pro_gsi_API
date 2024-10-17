from rest_framework import serializers
from .models import Categoria, Pedido, Usuario1

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']  # Especificamos los campos que queremos incluir


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'  # Incluye todos los campos del modelo Pedido


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario1
        fields = ('id', 'username', 'password', 'email', 'is_admin')  # Incluir is_admin

    def create(self, validated_data):
        user = Usuario1(**validated_data)
        user.save()
        return user
