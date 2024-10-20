from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='idCategoria')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calcular_monto_total(self):
        # Recalcula el total de los detalles en el back-end
        self.monto_total = sum(detalle.total for detalle in self.detalles.all())
        self.save()

    def __str__(self):
        return f"Pedido {self.id} - {self.nombre}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    product_id = models.IntegerField()
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle del Pedido {self.pedido.id} - Producto {self.product_id}"


class Usuario1Manager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Crear y devolver un usuario con un correo electrónico y contraseña."""
        if not email:
            raise ValueError('Los usuarios deben tener una dirección de correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crear y devolver un superusuario con un correo electrónico y contraseña."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        
        user = self.create_user(email, password, **extra_fields)
        
        default_permissions = ['can_view_user', 'can_edit_user']
        for perm in default_permissions:
            permission = Permission.objects.get(codename=perm)
            user.user_permissions.add(permission)
        return self.create_user(email, password, **extra_fields)




class Usuario1(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)  # Campo para distinguir administradores
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    REQUIRED_FIELDS = []
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    objects = Usuario1Manager()
    
    def __str__(self):
        return self.email

    @property
    def is_anonymous(self):
        return False  # Siempre devuelve False porque este objeto es un usuario autenticado.

    @property
    def is_authenticated(self):
        return True  # Siempre devuelve True porque este objeto es un usuario autenticado.

    class Meta:
        permissions = [
            ('can_view_user', 'Puede ver usuario'),
            ('can_edit_user', 'Puede editar usuario'),
        ]