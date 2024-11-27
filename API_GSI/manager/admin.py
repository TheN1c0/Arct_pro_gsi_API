from django.contrib import admin
from .models import Producto, Categoria, Pedido, DetallePedido, Usuario1
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin

# Registrar tus otros modelos
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Pedido)
admin.site.register(DetallePedido)

# Formulario personalizado para la creación de usuarios
class Usuario1CreationForm(UserCreationForm):
    class Meta:
        model = Usuario1
        fields = ('email', 'username', 'is_active', 'is_staff')  # Campos del modelo a mostrar

# Formulario personalizado para la edición de usuarios
class Usuario1ChangeForm(UserChangeForm):
    class Meta:
        model = Usuario1
        fields = ('email', 'username', 'is_active', 'is_staff', 'is_admin')  # Campos para edición

# Personalización del administrador del usuario
class Usuario1Admin(UserAdmin):
    # Usamos los formularios personalizados
    add_form = Usuario1CreationForm
    form = Usuario1ChangeForm
    
    # Campos que aparecerán en el formulario de creación y edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('username', 'is_active', 'is_staff', 'is_admin')}),
        ('Permisos', {'fields': ('is_superuser', 'user_permissions')}), 
    )
    
    # Campos que se mostrarán en la lista del admin
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_admin')
    list_filter = ('is_active', 'is_staff', 'is_admin', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('user_permissions',)
    
    # Configuración para la creación de superusuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin'),
        }),
    )

# Registrar el modelo Usuario1 con su configuración en el admin
admin.site.register(Usuario1, Usuario1Admin)
