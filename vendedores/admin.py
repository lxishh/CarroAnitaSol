from django.contrib import admin
from .models import Usuario, Propietaria, Vendedora

# Registro básico de los modelos
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'telefono', 'direccion')
    search_fields = ('usuario__username', 'rol', 'telefono')

@admin.register(Propietaria)
class PropietariaAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'ingresos_totales')
    search_fields = ('perfil__usuario__username',)

@admin.register(Vendedora)
class VendedoraAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'fecha_contratacion', 'ingresos_totales')
    search_fields = ('perfil__usuario__username',)
