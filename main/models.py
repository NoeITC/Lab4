from django.db import models
from django.contrib.auth.models import User


#Creamos la clase predeterminada Profile , a partir de ella se crean Cliente y Colaborador
class Profile(models.Model):
    # Relacion con el modelo User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Atributos adicionales para el usuario
    documento_identidad = models.CharField(max_length=8)
    fecha_nacimiento = models.DateField()
    estado = models.CharField(max_length=3)
    ## Opciones de genero donde yo quiero que se puedan seleccionar ciertas opciones de una lista desplegable
    MASCULINO = 'MA' ## variables tipo string, con estas variables hare mi lista de opciones
    FEMENINO = 'FE'
    NO_BINARIO = 'NB'
    GENERO_CHOICES = [   #lista de opciones(variable,level), tengo 1 tupla
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
        (NO_BINARIO, 'No Binario')
    ]
    genero = models.CharField(max_length=2, choices=GENERO_CHOICES)  #choices igual a lista de opciones

    def __str__(self): #metodo string, para mostrar nombre de usuario. Self para hacer referencia a Profile
        return self.user.get_username()

#Creamos la clase Cliente
class Cliente(models.Model):
    # Relacion con el modelo Perfil
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    # Atributos especificos del Cliente
    preferencias = models.ManyToManyField(to='Categoria')

    def __str__(self):
        return f'Cliente: {self.user_profile.user.get_username()}'

#Creamos la clase Colaborador
class Colaborador(models.Model):
    # Relacion con el modelo Perfil
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    # Atributos especificos del Colaborador
    reputacion = models.FloatField()
    cobertura_entrega = models.ManyToManyField(to='Localizacion')  # manytomanyfiel es lista de colab

    def __str__(self):
        return f'Repartidor: {self.user_profile.user.get_username()}'

#Creamos la clase Proveedor
class Proveedor(models.Model):
    #Atributos especifico de proveedor
    ruc = models.CharField(max_length=11)
    razon_social = models.CharField(max_length=20)
    telefono = models.CharField(max_length=9)

    def __str__(self):
        return self.razon_social

#Creamos la clase categoria
class Categoria(models.Model):
    #Atributos especificos de Categoria
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=50)


    def __str__(self):
        return f'{self.codigo}:{self.nombre}'

#Creamos la clase Localización
class Localizacion(models.Model):
    #Atributos especificos para Localizacion
    distrito = models.CharField(max_length=20)
    provincia = models.CharField(max_length=20)
    departamento = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.distrito}:{self.provincia}:{self.departamento}'

# Create your models here.
class Producto(models.Model):
    # Relaciones con Categoria y Proveedor
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

    # Atributos espeficicos de Producto
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField()
    precio = models.FloatField()
    estado = models.CharField(max_length=3)
    descuento = models.FloatField(default=0)

    #Metodo para calcular el precio final del producto
    def get_precio_final(self):
        return self.precio * (1 - self.descuento)
    #Metodo para generar un codigo único de producto_SKU (más complejo) con los codigos de categoria y producto
    def sku(self):
      codigo_categoria = self.categoria.codigo.zfill(4)
      codigo_producto = str(self.id).zfill(6)

      return f'{codigo_categoria}-{codigo_producto}'

#Creamos la clase pedido
class Pedido(models.Model):
    # Relaciones con  Cliente , Colaborador y Ubicacion
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    repartidor = models.ForeignKey('Colaborador', on_delete=models.SET_NULL, null=True)
    ubicacion = models.ForeignKey('Localizacion', on_delete=models.SET_NULL, null=True)

    # Atributos especificos de Pedido
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=3)
    direccion_entrega = models.CharField(max_length=100, blank=True, null=True)
    tarifa = models.FloatField(blank=True, null=True)

    #Atributos que se van a mostrar
    def __str__(self):
        return f'{self.cliente} - {self.fecha_creacion} - {self.estado}'

    #Método  para totalizar todos los subtotales de cada detalledepedido en el pedido ,
    #añadiendole la tarifa de envio
    def get_total(self):
        detalles = self.detallepedido_set.all()
        total = 0
        for detalle in detalles:
            total += detalle.get_subtotal()
        total += self.tarifa
        return total

#Creamos la clase DetallePedido
class DetallePedido(models.Model):
    # Relaciones con Producto y Pedido
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)

    # Atributos especifios de Detalle de Pedido
    cantidad = models.IntegerField(blank=True, null=True)

    #Atributos que se van a mostrar
    def __str__(self):
        return f'{self.pedido.id} - {self.cantidad} x {self.producto.nombre}'
    #Método para calcular el total por producto
    def get_subtotal(self):
        return self.producto.get_precio_final() * self.cantidad

#Creamos la clase ProductoImage
#nos permitira adjuntar varias imagenes por producto
class ProductoImage(models.Model):
    #Relaciones con Producto
    product = models.ForeignKey('Producto', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="products", null=True, blank=True)# podremos almacenar las imagenes en la carpeta products
