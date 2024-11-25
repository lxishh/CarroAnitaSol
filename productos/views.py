from django.shortcuts import render, redirect
from productos.forms import FormularioProducto
from productos.models import Producto, Categoria

# Create your views here.
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
    context = {'form':form}
    return render(request, 'form_producto.html', context)

#read
def listar_productos(request):
    # Filtro por nombre de categoría
    categoria = request.GET.get('categoria', None)  

    # Obtener todos los productos
    productos = Producto.objects.all()
    
    # Filtrar productos por nombre de categoría si se especifica
    if categoria:
        productos = productos.filter(categoria__nombre=categoria)

    # Obtener las categorías distintas para los filtros
    categorias = Categoria.objects.values_list('nombre', flat=True).distinct()

    # Pasar los productos y las categorías al contexto
    context = {
        'productos': productos,
        'categorias': categorias,
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
    context = {'form':form}
    return render(request, 'form_producto.html', context)

#delete
def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('productos')