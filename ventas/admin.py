from django.contrib import admin
from .models import Venta, DetalleVenta

# Registro del modelo Venta
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1  # Número de formularios vacíos para agregar detalles de venta

class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendedora', 'fecha', 'total')  # Campos que se mostrarán en la lista
    search_fields = ('vendedora__user__username', 'fecha')  # Permite buscar por el nombre de usuario de la vendedora o la fecha
    inlines = [DetalleVentaInline]  # Agrega el formulario para los detalles de la venta en la misma página

# Registro del modelo Venta en el admin
admin.site.register(Venta, VentaAdmin)

# Registro del modelo DetalleVenta (si quieres tener acceso directo desde el admin)
admin.site.register(DetalleVenta)
