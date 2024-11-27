from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Venta, DetalleVenta
from inventario.models import Inventario
from .forms import VentaForm, DetalleVentaForm

def agregar_venta(request):
    DetalleVentaFormSet = modelformset_factory(DetalleVenta, form=DetalleVentaForm, extra=1, can_delete=True)
    
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_formset = DetalleVentaFormSet(request.POST)

        if venta_form.is_valid() and detalle_formset.is_valid():
            # Guardar la venta
            venta = venta_form.save(commit=False)
            venta.total = 0  # Inicializa el total
            venta.save()

            # Guardar los detalles de la venta
            for form in detalle_formset:
                detalle = form.save(commit=False)
                detalle.venta = venta

                # Recuperar el precio unitario desde el producto
                if detalle.producto:
                    detalle.precio_unitario = detalle.producto.precio  # Suponiendo que el precio está en el modelo Producto

                # Verificar stock
                inventario = Inventario.objects.get(producto=detalle.producto)
                if inventario.stock_actual < detalle.cantidad:
                    venta.delete()  # Deshacer la venta
                    return render(request, 'agregar_venta.html', {
                        'venta_form': venta_form,
                        'detalle_formset': detalle_formset,
                        'error': f"Stock insuficiente para {detalle.producto.nombre}.",
                    })
                
                # Actualizar stock
                inventario.stock_actual -= detalle.cantidad
                inventario.save()

                # Calcular total de la venta
                venta.total += detalle.cantidad * detalle.precio_unitario
                detalle.save()

            venta.save()  # Guardar el total final
            return redirect('ventas')  # Redirigir a la lista de ventas

    else:
        venta_form = VentaForm()
        detalle_formset = DetalleVentaFormSet(queryset=DetalleVenta.objects.none())

    return render(request, 'agregar_venta.html', {
        'venta_form': venta_form,
        'detalle_formset': detalle_formset,
    })



#read
def listar_ventas(request):
    # Obtener todas las ventas
    ventas = Venta.objects.all()

    # Obtener el valor de la fecha para determinar el orden
    fecha = request.GET.get('fecha', 'asc')  # Por defecto es 'asc'

    # Ordenar las ventas según la opción seleccionada
    if fecha == 'asc':
        ventas = ventas.order_by('fecha')  # Ascendente
    elif fecha == 'desc':
        ventas = ventas.order_by('-fecha')  # Descendente


    context = {'ventas': ventas}
    
    # Pasar las ventas al template
    return render(request, 'ventas.html', context)