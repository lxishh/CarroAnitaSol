from django import forms
from .models import Inventario, MovimientoInventario

class FormularioInventario(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto', 'stock_actual']

class FormularioMovimientoInventario(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['inventario', 'tipo', 'cantidad', 'fecha', 'descripcion']
