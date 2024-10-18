from django.contrib import admin
from .models import Producto, Categoria, Pedido, DetallePedido,Usuario1
# Register your models here.
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Usuario1)


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('idProducto', 'nombre', 'price', 'stock', 'categoria')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('idCategoria', 'nombre', 'descripcion')
