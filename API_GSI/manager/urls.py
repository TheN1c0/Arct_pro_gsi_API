from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordResetView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    
)
urlpatterns = [
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/productos/<int:idProducto>/', ProductoAPIView.as_view(), name='producto-detail'),  # Para obtener, actualizar o eliminar un producto específico
    path('api/actualizar-stock/', ActualizarStockView.as_view(), name='actualizar_stock'),
    path('api/categorias/', ActualizarCategorias.as_view(), name='actualizar_categorias'),  # Para GET y POST
    path('api/categorias/<int:id>/', ActualizarCategorias.as_view(), name='actualizar_categoria'),  # Para PUT y DELETE
    path('api/pedidos/', ActualizarPedidos.as_view(), name='actualizar_pedidos'),  # Para GET y POST
    path('api/pedidos/<int:id>/', ActualizarPedidos.as_view(), name='actualizar_pedidos'),  # Para PUT y DELETE
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/usuarios/', UsuarioCreateView.as_view(), name='crear_usuario'),
    path('api/password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/productos/', ProductoAPIView.as_view(), name='producto-list'),  # Para obtener la lista de productos o crear uno nuevo
    path('api/enviar_reset_password/', enviar_reset_password, name='enviar_reset_password'),  # Para obtener la lista de productos o crear uno nuevo
    path('api/cambiar_contrasena/<slug:uid>/<str:token>/', CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
    path('api/detalles_pedido/', DetallePedidoAPIView.as_view(), name='detalles_pedido'),
    path('api/crear_pedidos/', CrearPedidoView.as_view(), name='crear_pedidos'),
    path('api/ver_pedidos/', PedidoAPIView.as_view(), name='ver_pedidos'),
    path('api/eliminar_pedidos/', EliminarPedidosView.as_view(), name='eliminar_pedidos'),
    path('api/ver_detalles/<int:idPedido>/', DetallePedidoAPIView.as_view(), name='ver_detalles'),

]

