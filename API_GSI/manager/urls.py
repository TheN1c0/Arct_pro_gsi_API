from django.urls import path
from .views import ActualizarStockView, CrearCategoriaView

urlpatterns = [
    path('api/actualizar-stock/', ActualizarStockView.as_view(), name='actualizar_stock'),
    path('api/categorias/', CrearCategoriaView.as_view(), name='crear-categoria'),
]