from django.db import models
from django.utils.timezone import now
from productos.models import Producto

class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)  # Cada producto tiene un inventario único
    stock_actual = models.IntegerField(default=0)  # Cantidad disponible

    def __str__(self):
        return f"{self.producto.nombre} - Stock: {self.stock_actual}"

class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)  # Entrada o salida
    cantidad = models.IntegerField()  # Cantidad movida
    fecha = models.DateTimeField(default=now)  # Fecha del movimiento
    descripcion = models.TextField(blank=True, null=True)  # Opcional: razón del movimiento

    def __str__(self):
        return f"{self.tipo.capitalize()} - {self.cantidad} - {self.inventario.producto.nombre}"
