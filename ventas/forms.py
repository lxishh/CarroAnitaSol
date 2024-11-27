from django import forms
from .models import Venta, DetalleVenta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['vendedora']  # Incluimos solo los campos que el usuario debe llenar.


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']  # Eliminamos el precio_unitario del formulario