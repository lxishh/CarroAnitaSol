from django.shortcuts import render, redirect

from vendedores.models import Usuario
from .forms import CrearUsuarioForm


#usuario/propietaria/vendedora

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
    return render(request, 'form.html', context)


# Listar todas las vendedoras
def listar_vendedores(request):
    usuarios = Usuario.objects.all()
    return render(request, 'vendedores.html', {'usuarios': usuarios})