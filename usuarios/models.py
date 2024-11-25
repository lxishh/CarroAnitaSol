from django.db import models
from django.contrib.auth.models import User

# Perfil general para usuarios (Propietarias y Vendedoras)
class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ROL_CHOICES = [
        ('Propietaria', 'Propietaria'),
        ('Vendedora', 'Vendedora'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)

    def __str__(self):
        return f"{self.usuario.username} ({self.rol})"

# Datos específicos para Propietarias
class Propietaria(models.Model):
    perfil = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    ingresos_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Propietaria: {self.perfil.usuario.username}"

# Datos específicos para Vendedoras
class Vendedora(models.Model):
    perfil = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_contratacion = models.DateField(blank=True, null=True)
    ingresos_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Para rastrear ventas

    def __str__(self):
        return f"Vendedora: {self.perfil.usuario.username}"