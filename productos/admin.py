from django.contrib import admin
from .models import Categoria, Producto

# Registrar el modelo Categoria en el admin
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')  # Muestra las columnas en el admin
    search_fields = ('nombre',)  # Permite la búsqueda por nombre
    list_filter = ('nombre',)  # Filtro por nombre de categoría
    ordering = ('nombre',)  # Ordena por nombre de categoría

# Registrar el modelo Producto en el admin
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'fecha_ingreso')  # Muestra estas columnas
    search_fields = ('nombre',)  # Permite la búsqueda por nombre
    list_filter = ('categoria',)  # Filtro por categoría
    ordering = ('nombre',)  # Ordena por nombre del producto
