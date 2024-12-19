import locale
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import Venta, DetalleVenta
from inventario.models import Inventario
from .forms import VentaForm, DetalleVentaForm
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth

from django.contrib.auth.decorators import login_required
from usuarios.utils import rol_requerido


def agregar_venta(request):
    DetalleVentaFormSet = modelformset_factory(
        DetalleVenta, form=DetalleVentaForm, extra=1, can_delete=True)

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
                if form.is_valid():  # Aseguramos que cada formulario sea válido
                    detalle = form.save(commit=False)
                    detalle.venta = venta

                    # Recuperar el precio unitario desde el producto
                    if detalle.producto:
                        # Suponiendo que el precio está en el modelo Producto
                        detalle.precio_unitario = detalle.producto.precio

                    # Verificar stock
                    try:
                        inventario = Inventario.objects.get(
                            producto=detalle.producto)
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

                    except Inventario.DoesNotExist:
                        # Si el producto no existe en inventario
                        venta.delete()  # Deshacer la venta
                        return render(request, 'agregar_venta.html', {
                            'venta_form': venta_form,
                            'detalle_formset': detalle_formset,
                            'error': f"No se encuentra inventario para {detalle.producto.nombre}.",
                        })

            venta.save()  # Guardar el total final
            return redirect('ventas')  # Redirigir a la lista de ventas

    else:
        venta_form = VentaForm()
        detalle_formset = DetalleVentaFormSet(
            queryset=DetalleVenta.objects.none())  # Formset vacío al cargar

    return render(request, 'agregar_venta.html', {
        'venta_form': venta_form,
        'detalle_formset': detalle_formset,
    })


# read
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


locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')


@login_required
@rol_requerido('Propietaria')
def ingresos(request):
    # Ingresos totales por día
    ingresos_dia = Venta.objects.annotate(dia=TruncDay(
        'fecha')).values('dia').annotate(total=Sum('total'))

    # Ingresos totales por semana
    ingresos_semana = Venta.objects.annotate(semana=TruncWeek(
        'fecha')).values('semana').annotate(total=Sum('total'))

    # Ingresos totales por mes
    ingresos_mes = Venta.objects.annotate(mes=TruncMonth(
        'fecha')).values('mes').annotate(total=Sum('total'))

    # Total general
    total_general = Venta.objects.aggregate(total=Sum('total'))['total']

    # Redondear los valores a enteros
    for ingreso in ingresos_dia:
        ingreso['total'] = round(ingreso['total'])

    for ingreso in ingresos_semana:
        ingreso['total'] = round(ingreso['total'])

    for ingreso in ingresos_mes:
        ingreso['total'] = round(ingreso['total'])

    # Formatear las fechas antes de pasar al template
    for ingreso in ingresos_dia:
        ingreso['dia'] = ingreso['dia'].strftime(
            '%d %b %Y').capitalize()  # Día en formato '28 Nov 2024'

    for ingreso in ingresos_semana:
        semana = ingreso['semana'].strftime(
            '%W, %Y')  # Semana en formato '48, 2024'
        # Semana 48 2024
        ingreso['semana'] = f"Semana {semana.split(',')[0]} de {semana.split(',')[1]}"

    for ingreso in ingresos_mes:
        # Mes en formato 'Noviembre 2024'
        mes = ingreso['mes'].strftime('%B %Y')
        # Asegurarse de que el mes comience con mayúscula
        ingreso['mes'] = mes.capitalize()

    # Pasar los datos al template
    context = {
        'ingresos_dia': ingresos_dia,
        'ingresos_semana': ingresos_semana,
        'ingresos_mes': ingresos_mes,
        'total_general': total_general,
    }
    return render(request, 'ingresos.html', context)
