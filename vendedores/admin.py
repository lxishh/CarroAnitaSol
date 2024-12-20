from django.contrib import admin
from .models import Usuario
from .forms import CrearUsuarioForm


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    form = CrearUsuarioForm
    list_display = ('rut', 'telefono', 'rol', 'fecha_contratacion')
