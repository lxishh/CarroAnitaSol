from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    ROL_CHOICES = [
        ('Propietaria', 'Propietaria'),
        ('Vendedora', 'Vendedora'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    fecha_contratacion = models.DateField(
        blank=True, null=True)  # Solo aplicable a vendedoras

    def __str__(self):
        return f"{self.usuario.username} ({self.rol})"
