from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Producto
from .serializers import CategoriaSerializer
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

class CrearCategoriaView(APIView):
    def post(self, request, *args, **kwargs):
        # Creamos un serializer con los datos del request
        serializer = CategoriaSerializer(data=request.data)
        
        # Validamos los datos
        if serializer.is_valid():
            serializer.save()  # Guardamos la nueva categoría
            return Response({
                'message': 'Categoría creada correctamente',
                'categoria': serializer.data  # Retornamos los datos de la categoría creada
            }, status=status.HTTP_201_CREATED)
        
        # Si hay un error en la validación, retornamos los errores
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
