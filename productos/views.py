from django.shortcuts import render, redirect
from productos.forms import FormularioProducto, FormularioCategoria
from productos.models import Producto, Categoria
from django.contrib import messages

from usuarios.models import Usuario

#create
def registrar_producto(request):
    form = FormularioProducto()
    if request.method == 'POST':
        form = FormularioProducto(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = FormularioProducto()
    context = {'form':form, 'titulo': 'Registrar Producto', 'icono': 'fas fa-plus-circle'}
    return render(request, 'form.html', context)

#read: aqui se utiliza categorias (para el filtro) e inventario (para la cantidad que hay en stock)
def listar_productos(request):
    try:
        # Obtener el perfil del usuario relacionado con el usuario autenticado
        usuario = Usuario.objects.get(usuario=request.user)
        rol = usuario.rol  # Obtener el rol (Propietaria o Vendedora)
    except Usuario.DoesNotExist:
        rol = None  # Si no existe un perfil, asignamos None
        
    # Obtener todos los productos
    productos = Producto.objects.select_related('categoria', 'inventario')

    # Filtro por nombre de categoría
    categoria = request.GET.get('categoria', None)  

    # Filtrar productos por nombre de categoría si se especifica
    if categoria:
        productos = productos.filter(categoria__nombre=categoria)

    # Obtener las categorías distintas para los filtros
    categorias = Categoria.objects.values_list('nombre', flat=True).distinct()

    # Pasar los productos y las categorías al contexto
    context = {
        'productos': productos,
        'categorias': categorias,
        'rol': rol,
    }
    
    # Renderizar la página con el contexto
    return render(request, 'productos.html', context)

#update
def actualizar_producto(request, id):
    producto = Producto.objects.get(id=id)
    form = FormularioProducto(instance=producto)
    if request.method == 'POST':
        form = FormularioProducto(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = FormularioProducto(instance=producto)
    context = {'form':form, 'titulo': 'Actualizar Producto', 'icono': 'fas fa-edit'}
    return render(request, 'form.html', context)

#delete
def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('productos')


#categorias
def registrar_categoria(request):
    form = FormularioCategoria()
    if request.method == 'POST':
        form = FormularioCategoria(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos')  # Redirige a la página de productos después de guardar
        else:
            messages.error(request, 'Hubo un error al registrar la categoría.')
            return render(request, 'form.html', {'form': form})
    context = {'form':form, 'titulo': 'Registrar Categoria', 'icono': 'fas fa-plus-circle'}
    return render(request, 'form.html', context)