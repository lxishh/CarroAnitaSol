from django.shortcuts import get_object_or_404, render, redirect

from vendedores.models import Usuario
from .forms import ActualizarPerfilUsuarioForm, ActualizarUsuarioForm, CrearUsuarioForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from usuarios.utils import rol_requerido


#usuario/propietaria/vendedora

@login_required
@rol_requerido('Propietaria')
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


@login_required
@rol_requerido('Propietaria')
# Read
def listar_vendedores(request):
    usuarios = Usuario.objects.all()
    context = {'usuarios': usuarios}
    return render(request, 'vendedores.html', context)

@login_required
@rol_requerido('Propietaria')
def actualizar_vendedor(request, id):
    usuario = Usuario.objects.get(id=id)  # Obtener el perfil de usuario
    user = usuario.usuario  # Obtener el usuario asociado

    if request.method == 'POST':
        form_user = ActualizarUsuarioForm(request.POST, instance=user)
        form_perfil = ActualizarPerfilUsuarioForm(request.POST, instance=usuario)

        if form_user.is_valid() and form_perfil.is_valid():
            # Verificar si se ha introducido una nueva contraseña
            nueva_contrasena = form_user.cleaned_data.get('password')
            if nueva_contrasena:
                # Si hay una nueva contraseña, cifrarla
                user.set_password(nueva_contrasena)
            
            form_user.save()  # Guardar los cambios del usuario
            form_perfil.save()  # Guardar los cambios del perfil
            messages.success(request, 'Vendedor actualizado exitosamente.')
            return redirect('vendedores')  # Redirigir a la lista de vendedores

    else:
        form_user = ActualizarUsuarioForm(instance=user)
        form_perfil = ActualizarPerfilUsuarioForm(instance=usuario)

    context = {
        'form_user': form_user,
        'form_perfil': form_perfil,
        'titulo': 'Actualizar Vendedor',
        'icono': 'fas fa-edit',
        'usuario': usuario
    }
    return render(request, 'form_actualizar.html', context)


@login_required
@rol_requerido('Propietaria')
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