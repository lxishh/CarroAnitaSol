from django import forms
from .models import Venta, DetalleVenta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['vendedor']  # Incluimos solo los campos que el usuario debe llenar.


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']  # Eliminamos el precio_unitario del formulario

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')

        # Validación para que la cantidad sea al menos 1
        if cantidad < 1:
            raise forms.ValidationError('La cantidad debe ser al menos 1.')

        return cantidad