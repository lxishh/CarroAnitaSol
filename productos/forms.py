from django import forms
from productos.models import Producto, Categoria

class FormularioProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre', 'descripcion', 'precio', 'categoria')  
        labels = {
            'nombre': 'Nombre del producto:',
            'descripcion': 'Descripción:',
            'precio': 'Precio:',
            'categoria': 'Categoría:',
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        # Verifica si ya existe un producto con el mismo nombre
        if Producto.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError('Ya existe un producto con este nombre.')
        return nombre


class FormularioCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nombre', 'descripcion',)  # Elimina 'cantidad' porque no existe en el modelo
        labels = {
            'nombre': 'Nombre de la categoria:',
            'descripcion': 'Descripción:',
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        # Verifica si ya existe una categoría con el mismo nombre
        if Categoria.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError('Esta categoría ya existe.')
        return nombre