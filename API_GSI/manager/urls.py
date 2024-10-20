from django.urls import path
<<<<<<< HEAD
from .views import ActualizarStockView, ActualizarCategorias, ActualizarPedidos,UsuarioCreateView, ProductoAPIView
=======
from .views import ActualizarStockView, ActualizarCategorias, ActualizarPedidos,UsuarioCreateView, ProductosView
>>>>>>> 6a6ad23bfc153fd2f4e79165fba9899c157c859d
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
urlpatterns = [
    path('api/actualizar-stock/', ActualizarStockView.as_view(), name='actualizar_stock'),
    path('api/categorias/', ActualizarCategorias.as_view(), name='actualizar_categorias'),  # Para GET y POST
    path('api/categorias/<int:id>/', ActualizarCategorias.as_view(), name='actualizar_categoria'),  # Para PUT y DELETE
    path('api/pedidos/', ActualizarPedidos.as_view(), name='actualizar_pedidos'),  # Para GET y POST
    path('api/pedidos/<int:id>/', ActualizarPedidos.as_view(), name='actualizar_pedidos'),  # Para PUT y DELETE
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/usuarios/', UsuarioCreateView.as_view(), name='crear_usuario'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
<<<<<<< HEAD
    path('api/productos/', ProductoAPIView.as_view(), name='producto-list'),  # Para obtener la lista de productos o crear uno nuevo
    path('api/productos/<int:idProducto>/', ProductoAPIView.as_view(), name='producto-detail'),  # Para obtener, actualizar o eliminar un producto específico
=======
    path('api/productos/', ProductosView.as_view(), name='obtener_productos')
>>>>>>> 6a6ad23bfc153fd2f4e79165fba9899c157c859d

]

