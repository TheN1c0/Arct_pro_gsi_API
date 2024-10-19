from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *

from .models import Producto, Categoria, Pedido, Usuario1

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['idCategoria', 'nombre', 'descripcion']

class ActualizarStockView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            # Obtenemos los datos del request
            product_id = request.data.get('id')
            cantidad = request.data.get('cantidad')

            # Buscamos el producto en la base de datos
            producto = Producto.objects.get(idProducto=product_id)
            
            # Actualizamos el stock del producto
            producto.stock += int(cantidad)
            producto.save()

            return Response({
                'message': 'Stock actualizado correctamente',
                'producto': producto.nombre,
                'nuevo_stock': producto.stock
            }, status=status.HTTP_200_OK)

        except Producto.DoesNotExist:
            return Response({
                'error': 'Producto no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

class ActualizarCategorias(APIView):
    
    def get(self, request, *args, **kwargs):
        try:
            # Obtiene todas las categorías de la base de datos
            categorias = list(Categoria.objects.values('idCategoria', 'nombre', 'descripcion', 'created_at', 'updated_at'))

            # Devuelve la lista de categorías como un JSON
            return Response({'categorias': categorias}, status=status.HTTP_200_OK)  # Estado 200 OK
        except Exception as e:  # Captura cualquier excepción que ocurra
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Estado 500 Internal Server Error

    def post(self, request, *args, **kwargs):
        # Utiliza el serializador para validar y crear una nueva categoría
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            categoria = serializer.save()  # Guarda la nueva categoría en la base de datos
            return Response({'mensaje': 'Categoría creada correctamente', 'categoria': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve errores si la validación falla
    
    def put(self, request, *args, **kwargs):
        # Actualiza una categoría existente
        try:
            categoria_id = kwargs.get('id')  # Obtiene el ID de la categoría de la URL
            categoria = Categoria.objects.get(idCategoria=categoria_id)  # Busca la categoría por ID
            serializer = CategoriaSerializer(categoria, data=request.data, partial=True)  # Serializa con los nuevos datos

            if serializer.is_valid():
                serializer.save()  # Guarda los cambios en la base de datos
                return Response({'mensaje': 'Categoría actualizada correctamente', 'categoria': serializer.data}, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve errores si la validación falla
        except Categoria.DoesNotExist:
            return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)  # Manejo de error si la categoría no existe

    def delete(self, request, *args, **kwargs):
        # Elimina una categoría existente
        try:
            categoria_id = kwargs.get('id')  # Obtiene el ID de la categoría de la URL
            categoria = Categoria.objects.get(idCategoria=categoria_id)  # Busca la categoría por ID
            categoria.delete()  # Elimina la categoría
            return Response({'mensaje': 'Categoría eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)
        except Categoria.DoesNotExist:
            return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)  # Manejo de error si la categoría no existe



class ActualizarPedidos(APIView):
    
    def get(self, request, *args, **kwargs):
        try:
            # Obtiene todos los pedidos de la base de datos
            pedidos = list(Pedido.objects.values('id', 'nombre', 'apellido', 'estado', 'monto_total', 'created_at', 'updated_at'))

            # Devuelve la lista de pedidos como un JSON
            return Response({'pedidos': pedidos}, status=status.HTTP_200_OK)  # Estado 200 OK
        except Exception as e:  # Captura cualquier excepción que ocurra
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Estado 500 Internal Server Error

    def post(self, request, *args, **kwargs):
        # Utiliza el serializador para validar y crear un nuevo pedido
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            pedido = serializer.save()  # Guarda el nuevo pedido en la base de datos
            return Response({'mensaje': 'Pedido creado correctamente', 'pedido': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve errores si la validación falla
    
    def put(self, request, *args, **kwargs):
        # Actualiza un pedido existente
        try:
            pedido_id = kwargs.get('id')  # Obtiene el ID del pedido de la URL
            pedido = Pedido.objects.get(id=pedido_id)  # Busca el pedido por ID
            serializer = PedidoSerializer(pedido, data=request.data, partial=True)  # Serializa con los nuevos datos

            if serializer.is_valid():
                serializer.save()  # Guarda los cambios en la base de datos
                return Response({'mensaje': 'Pedido actualizado correctamente', 'pedido': serializer.data}, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve errores si la validación falla
        except Pedido.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)  # Manejo de error si el pedido no existe

    def delete(self, request, *args, **kwargs):
        # Elimina un pedido existente
        try:
            pedido_id = kwargs.get('id')  # Obtiene el ID del pedido de la URL
            pedido = Pedido.objects.get(id=pedido_id)  # Busca el pedido por ID
            pedido.delete()  # Elimina el pedido
            return Response({'mensaje': 'Pedido eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
        except Pedido.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)  # Manejo de error si el pedido no existe

# API para obtener el token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# API para verificar si el token es válido
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Authorized'})
    
from rest_framework import generics
from .models import Usuario1
from .serializers import UsuarioSerializer

class UsuarioCreateView(generics.CreateAPIView):
    queryset = Usuario1.objects.all()
    serializer_class = UsuarioSerializer

class ProductosView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            productos = list(Producto.objects.values('idProducto', 'nombre', 'descripcion', 'price', 'stock', 'categoria'))
            return Response({'productos': productos}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
