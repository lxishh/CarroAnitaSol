from django.shortcuts import get_object_or_404, render, redirect

from vendedores.models import Usuario
from .forms import CrearUsuarioForm

from django.contrib import messages


#usuario/propietaria/vendedora

# Create
def crear_vendedor(request):
    form = CrearUsuarioForm()
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendedores')  # Redirige a una lista de usuarios
    else:
        form = CrearUsuarioForm()
    context = {'form':form, 'titulo': 'Registrar Vendedor', 'icono': 'fas fa-plus-circle'}
    return render(request, 'form_vendedores.html', context)


# Read
def listar_vendedores(request):
    usuarios = Usuario.objects.all()
    context = {'usuarios': usuarios}
    return render(request, 'vendedores.html', context)

#Update
def actualizar_vendedor(request, id):
    usuario = Usuario.objects.get(id=id)  # Obtener el usuario por su id
    form = CrearUsuarioForm(instance=usuario)
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()  # Guarda los cambios en el perfil y en el usuario de Django
            return redirect('vendedores')  # Redirige a la lista de vendedores
    else:
        form = CrearUsuarioForm(instance=usuario)

    context = {
        'form': form,
        'titulo': 'Actualizar Vendedor',
        'icono': 'fas fa-edit',
        'usuario': usuario
    }
    return render(request, 'form_vendedores.html', context)

#delete
def eliminar_vendedor(request, id):
    try:
        usuario = get_object_or_404(Usuario, pk=id)
        user = usuario.usuario  # Verifica que exista la relación
        usuario.delete()  # Elimina el perfil de Usuario
        user.delete()  # Elimina el usuario de Django
        messages.success(request, 'El vendedor ha sido eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar el vendedor: {e}')
    return redirect('vendedores')  # Asegúrate de que esta ruta sea correcta