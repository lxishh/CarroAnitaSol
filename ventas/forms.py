from django import forms
from .models import Venta, DetalleVenta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['vendedora', 'fecha', 'total']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['venta', 'producto', 'cantidad', 'precio_unitario']
