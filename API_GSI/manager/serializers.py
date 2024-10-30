from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']  # Especificamos los campos que queremos incluir


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'  # Incluye todos los campos del modelo Pedido
        

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['idProducto', 'nombre', 'descripcion', 'price', 'stock', 'categoria']  # Incluye todos los campos necesarios



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregar datos personalizados al token
        token['email'] = user.email
        token['is_admin'] = user.is_admin
        return token

    # Aquí puedes personalizar cómo se validan las credenciales
    def validate(self, attrs):
        try:
            user = Usuario1.objects.get(email=attrs['email'])
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError("Credenciales incorrectas")
        except Usuario1.DoesNotExist:
            raise serializers.ValidationError("Usuario no encontrado")
        
        # Generar el token
        return super().validate(attrs)

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario1
        fields = ['username', 'email', 'password', 'is_admin']  # Puedes incluir otros campos si es necesario
        extra_kwargs = {'password': {'write_only': True}}  # Asegúrate de que la contraseña no se devuelva en la respuesta

    def create(self, validated_data):
        # Crea el usuario sin eliminar el campo 'password'
        user = Usuario1(**validated_data)
        user.save()  # Aquí se llama al método save del modelo que encripta la contraseña
        return user

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = ['id', 'pedido', 'product_id', 'cantidad', 'precio', 'total']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['nombre', 'apellido', 'estado', 'monto_total', 'detalles']