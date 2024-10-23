from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from .models import Producto, Categoria, Pedido, Usuario1
from .serializers import ProductoSerializer 

from django.http import JsonResponse
from .models import Producto
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Usuario1  # Asegúrate de importar tu modelo de usuario personalizado
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import make_password

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

 # Asegúrate de que este serializer esté definido

class ProductoAPIView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            # Obtiene todos los productos de la base de datos
            productos = list(Producto.objects.values('idProducto', 'nombre', 'descripcion', 'price', 'stock', 'categoria', 'created_at', 'updated_at'))

            # Devuelve la lista de productos como un JSON
            return Response({'productos': productos}, status=status.HTTP_200_OK)  # Estado 200 OK
        except Exception as e:  # Captura cualquier excepción que ocurra
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Estado 500 Internal Server Error

    def post(self, request, *args, **kwargs):
        # Utiliza el serializador para validar y crear un nuevo producto
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            producto = serializer.save()  # Guarda el nuevo producto en la base de datos
            return Response({'mensaje': 'Producto creado correctamente', 'producto': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve errores si la validación falla

    def put(self, request, *args, **kwargs):
        # Actualiza un producto existente
        try:
            producto_id = kwargs.get('idProducto')  # Obtiene el ID del producto de la URL
            producto = Producto.objects.get(idProducto=producto_id)  # Busca el producto por ID
            serializer = ProductoSerializer(producto, data=request.data, partial=True)  # Serializa con los nuevos datos

            if serializer.is_valid():
                serializer.save()  # Guarda los cambios en la base de datos
                return Response({'mensaje': 'Producto actualizado correctamente', 'producto': serializer.data}, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve errores si la validación falla
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)  # Manejo de error si el producto no existe

    def delete(self, request, *args, **kwargs):
        # Elimina un producto existente
        try:
            producto_id = kwargs.get('idProducto')  # Obtiene el ID del producto de la URL
            producto = Producto.objects.get(idProducto=producto_id)  # Busca el producto por ID
            producto.delete()  # Elimina el producto
            return Response({'mensaje': 'Producto eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)  # Manejo de error si el producto no existe










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

class CambiarContrasenaView(APIView):
    def post(self, request, uid):
        try:
            # Obtén el usuario por uid
            usuario = Usuario1.objects.get(id=uid)
            nueva_contrasena = request.data.get('password')

            if nueva_contrasena:
                usuario.password = make_password(nueva_contrasena)
                usuario.save()
                return Response({'success': 'Contraseña cambiada con éxito.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'La contraseña no puede estar vacía.'}, status=status.HTTP_400_BAD_REQUEST)

        except Usuario1.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log del error
            logger.error(f'Error al cambiar la contraseña: {str(e)}')
            return Response({'error': 'Error al cambiar la contraseña.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductosView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            productos = list(Producto.objects.values('idProducto', 'nombre', 'descripcion', 'price', 'stock', 'categoria'))
            return Response({'productos': productos}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@csrf_exempt
def productos_api(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        productos_list = list(productos.values())
        return JsonResponse({'productos': productos_list}, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        nuevo_producto = Producto.objects.create(
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            price=data['price'],
            stock=data['stock'],
            categoria_id=1  # Asigna una categoría predeterminada
        )
        return JsonResponse({'message': 'Producto creado correctamente'}, status=201)

@csrf_exempt
def producto_detalle_api(request, producto_id):
    try:
        producto = Producto.objects.get(idProducto=producto_id)
    except Producto.DoesNotExist:
        return JsonResponse({'message': 'Producto no encontrado'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        producto.nombre = data['nombre']
        producto.descripcion = data['descripcion']
        producto.price = data['price']
        producto.stock = data['stock']
        producto.save()
        return JsonResponse({'message': 'Producto actualizado correctamente'})

    if request.method == 'DELETE':
        producto.delete()
        return JsonResponse({'message': 'Producto eliminado correctamente'})


@csrf_exempt 
def enviar_reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Verificar si el correo electrónico existe en la base de datos
        try:
            usuario = Usuario1.objects.get(email=email)
        except Usuario1.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Correo no registrado'}, status=400)

        # Generar el token de restablecimiento de contraseña
        token = default_token_generator.make_token(usuario)

        # Crear la URL para el restablecimiento de la contraseña
        uid = urlsafe_base64_encode(force_bytes(usuario.id))
        reset_url = f"http://127.0.0.1:8000/restablecer_contrasena/{uid}/{token}"

        # Enviar el correo con el enlace de restablecimiento
        subject = "Recuperación de Contraseña"
        message = f"Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Desde qué correo se enviará
            [email],
            fail_silently=False,
        )

        # Responder al usuario que el correo fue enviado
        return JsonResponse({'success': True, 'message': 'Revisa tu correo para continuar con el restablecimiento.'})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
