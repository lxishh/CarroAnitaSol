from django import forms
from productos.models import Producto

class FormularioProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre', 'descripcion', 'precio', 'categoria')  # Elimina 'cantidad' porque no existe en el modelo
        labels = {
            'nombre': 'Nombre del producto:',
            'descripcion': 'Descripción:',
            'precio': 'Precio:',
            'categoria': 'Categoría:',
        }

