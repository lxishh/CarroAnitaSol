from django.shortcuts import render, get_object_or_404, redirect
from ventas.models import Venta, DetalleVenta
from productos.models import Producto, Categoria
from ventas.forms import VentaForm, DetalleVentaForm  # Asegúrate de crear estos formularios

# Crear una venta
def crear_venta(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        if venta_form.is_valid():
            venta = venta_form.save()  # Guarda la venta
            # Crear los detalles de la venta
            for producto_id, cantidad in request.POST.items():
                if 'producto_' in producto_id:
                    producto_id = producto_id.split('_')[1]  # Extrae el ID del producto
                    producto = Producto.objects.get(id=producto_id)
                    DetalleVenta.objects.create(
                        venta=venta,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio
                    )
            return redirect('listar_ventas')  # Redirige a la lista de ventas
    else:
        venta_form = VentaForm()
    
    return render(request, 'ventas/crear_venta.html', {'venta_form': venta_form})

# Listar todas las ventas
def listar_ventas(request):
    ventas = Venta.objects.all()
    context = {'ventas':ventas}
    return render(request, 'ventas.html')

# Ver los detalles de una venta
def ver_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    detalles = DetalleVenta.objects.filter(venta=venta)
    return render(request, 'ventas/ver_venta.html', {'venta': venta, 'detalles': detalles})

# Actualizar una venta
def actualizar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta_form = VentaForm(request.POST, instance=venta)
        if venta_form.is_valid():
            venta_form.save()
            return redirect('listar_ventas')  # Redirige a la lista de ventas
    else:
        venta_form = VentaForm(instance=venta)
    
    return render(request, 'ventas/actualizar_venta.html', {'venta_form': venta_form})

# Eliminar una venta
def eliminar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('listar_ventas')  # Redirige a la lista de ventas
    
    return render(request, 'ventas/eliminar_venta.html', {'venta': venta})
