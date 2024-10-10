from django.urls import path
from .views import ActualizarStockView

urlpatterns = [
    path('api/actualizar-stock/', ActualizarStockView.as_view(), name='actualizar_stock'),
]