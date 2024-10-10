from django.contrib import admin
from .models import Producto, Categoria
# Register your models here.
admin.site.register(Producto)
admin.site.register(Categoria)


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('idProducto', 'nombre', 'price', 'stock', 'categoria')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('idCategoria', 'nombre', 'descripcion')
