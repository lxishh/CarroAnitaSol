from django.shortcuts import redirect, render

from inventario.forms import FormularioInventario
from inventario.models import Inventario

from django.contrib.auth.decorators import login_required
from usuarios.utils import rol_requerido

# Create your views here.
def registrar_inventario(request):
    form = FormularioInventario()
    if request.method == 'POST':
        form = FormularioInventario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')  # Redirige a la página de inventarios después de guardar
    context = {'form': form, 'titulo': 'Registrar Inventario', 'icono': 'fas fa-plus-circle'}
    return render(request, 'form_inventario.html', context)

def listar_inventarios(request):
    inventarios = Inventario.objects.all()
    context = {'inventarios': inventarios}
    return render(request, 'inventario.html', context)

def actualizar_inventario(request, id):
    inventario = Inventario.objects.get(id=id)
    form = FormularioInventario(instance=inventario)
    if request.method == 'POST':
        form = FormularioInventario(request.POST, instance=inventario)
        if form.is_valid():
            form.save()
            return redirect('inventario')  # Redirige a la página de inventarios después de guardar
    context = {'form': form, 'titulo': 'Actualizar Inventario', 'icono': 'fas fa-edit'}
    return render(request, 'form_inventario.html', context)

def eliminar_inventario(request, id):
    inventario = Inventario.objects.get(id=id)
    inventario.delete()
    return redirect('inventario')  # Redirige a la página de inventarios después de eliminar




# from django.shortcuts import render, redirect
# from .forms import FormularioMovimientoInventario
# from .models import MovimientoInventario

# def registrar_movimiento_inventario(request):
#     form = FormularioMovimientoInventario()
#     if request.method == 'POST':
#         form = FormularioMovimientoInventario(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('movimientos_inventario')  # Redirige a la página de movimientos de inventario después de guardar
#     context = {'form': form, 'titulo': 'Registrar Movimiento de Inventario', 'icono': 'fas fa-plus-circle'}
#     return render(request, 'form.html', context)

# from django.shortcuts import render
# from .models import MovimientoInventario

# def listar_movimientos_inventario(request):
#     movimientos = MovimientoInventario.objects.all()
#     context = {'movimientos': movimientos}
#     return render(request, 'movimientos_inventario.html', context)

# from django.shortcuts import render, redirect
# from .models import MovimientoInventario
# from .forms import FormularioMovimientoInventario

# def actualizar_movimiento_inventario(request, id):
#     movimiento = MovimientoInventario.objects.get(id=id)
#     form = FormularioMovimientoInventario(instance=movimiento)
#     if request.method == 'POST':
#         form = FormularioMovimientoInventario(request.POST, instance=movimiento)
#         if form.is_valid():
#             form.save()
#             return redirect('movimientos_inventario')  # Redirige a la página de movimientos de inventario después de guardar
#     context = {'form': form, 'titulo': 'Actualizar Movimiento de Inventario', 'icono': 'fas fa-edit'}
#     return render(request, 'form.html', context)

# from django.shortcuts import redirect
# from .models import MovimientoInventario

# def eliminar_movimiento_inventario(request, id):
#     movimiento = MovimientoInventario.objects.get(id=id)
#     movimiento.delete()
#     return redirect('movimientos_inventario')  # Redirige a la página de movimientos de inventario después de eliminar
