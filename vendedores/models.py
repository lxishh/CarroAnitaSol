from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    ROL_CHOICES = [
        ('Propietaria', 'Propietaria'),
        ('Vendedora', 'Vendedora'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    fecha_contratacion = models.DateField(blank=True, null=True)  # Solo aplicable a vendedoras
    ingresos_totales = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.usuario.username} ({self.rol})"