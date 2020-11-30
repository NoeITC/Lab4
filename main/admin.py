from django.contrib import admin#Importamos la interfaz de adminitrador
from .models import *# Importamos todas las clases de models.py


#Generamos las claseS ClienteInline , ColaboradorInline,ProfileAdmin para
#puedan visualizar nuestras clases Cliente, Colaborador y Profile en la pagina de
#administrador
class ClienteInline(admin.TabularInline):
    model=Cliente


class ColaboradorInline(admin.TabularInline):
    model=Colaborador


class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        ClienteInline,
        ColaboradorInline
    ]

#Generamos las clases ProfileAdmin y ProductoImageInline para facilitar la subida de varias imagenes por producto
class ProductoImageInline(admin.TabularInline):
    model=ProductoImage


class ProductoAdmin(admin.ModelAdmin):
    inlines = [
        ProductoImageInline,
    ]

# Registramos nuestros modelos aqui

admin.site.register(Cliente)
admin.site.register(Colaborador)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Localizacion)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
