from django.urls import path
from .views import ActualizarStockView, ActualizarCategorias, ActualizarPedidos

urlpatterns = [
    path('api/actualizar-stock/', ActualizarStockView.as_view(), name='actualizar_stock'),
    path('api/categorias/', ActualizarCategorias.as_view(), name='actualizar_categorias'),  # Para GET y POST
    path('api/categorias/<int:id>/', ActualizarCategorias.as_view(), name='actualizar_categoria'),  # Para PUT y DELETE
    path('api/pedidos/', ActualizarPedidos.as_view(), name='actualizar_pedidos'),  # Para GET y POST
    path('api/pedidos/<int:id>/', ActualizarPedidos.as_view(), name='actualizar_pedidos'),  # Para PUT y DELETE
]