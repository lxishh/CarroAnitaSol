from django.contrib import admin
from .models import Inventario, MovimientoInventario

class InventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'stock_actual')  # Muestra el producto y el stock en la lista
    search_fields = ('producto__nombre',)  # Permite buscar por el nombre del producto

class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('inventario', 'tipo', 'cantidad', 'fecha', 'descripcion')  # Muestra los detalles del movimiento
    list_filter = ('tipo', 'fecha')  # Filtros para tipo de movimiento y fecha
    search_fields = ('inventario__producto__nombre', 'descripcion')  # Permite buscar por producto o descripción

admin.site.register(Inventario, InventarioAdmin)
admin.site.register(MovimientoInventario, MovimientoInventarioAdmin)
