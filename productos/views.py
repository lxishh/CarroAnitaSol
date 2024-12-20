from django.shortcuts import render, redirect
from productos.forms import FormularioProducto, FormularioCategoria
from productos.models import Producto, Categoria
from django.contrib import messages

from vendedores.models import Usuario
from django.db import connection

# create


# Función para ejecutar procedimientos almacenados
# se define que se debe pasar el nombre del procedimiento y los parametros respectivos
def ejecutar_procedimiento(proc_nombre, params=()):
    with connection.cursor() as cursor:
        cursor.callproc(proc_nombre, params)
        # Solo obtener resultados si es un SELECT
        if proc_nombre in ['listar_productos']:
            return cursor.fetchall()
        return None

# Vista para listar productos usando el procedimiento almacenado


def listar_productos(request):
    # Ejecutar el procedimiento almacenado
    productos_raw = ejecutar_procedimiento('listar_productos')

    # Mapear los resultados a un formato adecuado
    productos = [
        {
            'id': p[0],
            'nombre': p[1],
            'codigo': p[2],
            'descripcion': p[3],
            'precio': p[4],
            'categoria': p[5],
            'cantidad': p[6],  # Aquí es donde se obtiene la cantidad
            'fecha_ingreso': p[7],
        }
        for p in productos_raw
    ]

    # Obtener las categorías para el filtro
    categorias = Categoria.objects.all()

    # Pasar los productos y las categorías al contexto
    context = {
        'productos': productos,
        'categorias': categorias,
    }

    return render(request, 'productos.html', context)


# Vista para registrar un producto usando el procedimiento almacenado
def registrar_producto(request):
    form = FormularioProducto()
    if request.method == 'POST':
        form = FormularioProducto(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            codigo = form.cleaned_data['codigo']
            descripcion = form.cleaned_data['descripcion']
            cantidad = form.cleaned_data['cantidad']
            precio = form.cleaned_data['precio']
            categoria_id = form.cleaned_data['categoria'].id

            # Incluye el campo código en el procedimiento almacenado
            ejecutar_procedimiento('registrar_producto', [
                                   nombre, codigo, descripcion, cantidad, precio, categoria_id])
            return redirect('/productos')

    context = {'form': form}
    return render(request, 'registrar_productos.html', context)


# Vista para actualizar un producto usando el procedimiento almacenado
def actualizar_producto(request, id):
    producto = Producto.objects.get(id=id)
    form = FormularioProducto(instance=producto)

    if request.method == 'POST':
        form = FormularioProducto(request.POST, instance=producto)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            codigo = form.cleaned_data['codigo']
            descripcion = form.cleaned_data['descripcion']
            cantidad = form.cleaned_data['cantidad']
            precio = form.cleaned_data['precio']
            categoria_id = form.cleaned_data['categoria'].id

            # Incluye el campo código en el procedimiento almacenado
            ejecutar_procedimiento('actualizar_producto', [
                                   id, nombre, codigo, descripcion, cantidad, precio, categoria_id])
            return redirect('/productos')

    context = {'form': form}
    return render(request, 'registrar_productos.html', context)


# Vista para eliminar un producto usando el procedimiento almacenado
def eliminar_producto(request, id):
    # Llamamos al procedimiento almacenado para eliminar el producto
    ejecutar_procedimiento('eliminar_producto', [id])
    return redirect('/productos')


# categorias
def registrar_categoria(request):
    form = FormularioCategoria()
    if request.method == 'POST':
        form = FormularioCategoria(request.POST)
        if form.is_valid():
            form.save()
            # Redirige a la página de productos después de guardar
            return redirect('categorias')
        else:
            messages.error(request, 'Hubo un error al registrar la categoría.')
            return render(request, 'form_categoria.html', {'form': form})
    context = {'form': form, 'titulo': 'Registrar Categoria',
               'icono': 'fas fa-plus-circle'}
    return render(request, 'form_categoria.html', context)


def listar_categorias(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    context = {'categorias': categorias}
    return render(request, 'categorias.html', context)


def actualizar_categoria(request, id):
    # Obtener la categoría a actualizar
    categoria = Categoria.objects.get(id=id)
    form = FormularioCategoria(instance=categoria)
    if request.method == 'POST':
        form = FormularioCategoria(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            # Redirige a la página de categorías después de guardar
            return redirect('categorias')
    context = {'form': form, 'titulo': 'Actualizar Categoria',
               'icono': 'fas fa-edit'}
    return render(request, 'form_categoria.html', context)


def eliminar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)  # Obtener la categoría a eliminar
    categoria.delete()
    # Redirige a la página de categorías después de eliminar
    return redirect('categorias')
