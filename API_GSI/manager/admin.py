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

class Usuario1Admin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'created_at', 'update_at')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')

    # Opcional: permite que los usuarios editen el modelo directamente en el admin
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password', 'is_active', 'is_staff')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    ordering = ('email',)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)