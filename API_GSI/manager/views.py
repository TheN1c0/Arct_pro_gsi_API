from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Producto, Categoria
from rest_framework import serializers

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['idCategoria', 'nombre', 'descripcion']

class ActualizarStockView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            # Obtenemos los datos del request
            product_id = request.data.get('idProducto')
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