from django.db import models
from django.utils.timezone import now

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre # Retorna el nombre de la categoría

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(default=now)
    
    def __str__(self):
        return f"{self.nombre} - {self.categoria.nombre}"  # Muestra el nombre del producto y la categoría
