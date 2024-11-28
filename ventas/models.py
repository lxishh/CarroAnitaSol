from django.db import models
from productos.models import Producto
from django.utils.timezone import now
from vendedores.models import Usuario

class Venta(models.Model):
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'Vendedora'})
    fecha = models.DateTimeField(default=now)  # Fecha de la venta
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total de la venta

    def __str__(self):
        return f"Venta de {self.vendedor.usuario.username} - Total: {self.total}"

    # Método para recalcular el total de la venta
    def calcular_total(self):
        total = sum(detalle.subtotal() for detalle in self.detalles.all())
        self.total = total
        self.save()  # Guardamos la venta con el nuevo total

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')  # Relación con la venta
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto vendido
    cantidad = models.IntegerField()  # Cantidad vendida
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Precio unitario del producto

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Venta #{self.venta.id})"

    # Override del método save para actualizar el total de la venta automáticamente
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guardar el detalle primero
        self.venta.calcular_total()  # Recalcular el total de la venta después de guardar el detalle
