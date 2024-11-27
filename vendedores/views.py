from django.shortcuts import render


#usuario/propietaria/vendedora

# Listar todos los vendedores
def listar_vendedores(request):
    #vendedores = Usuario.user.rol.vendedor (o algo asi)
    context = {'vendedores':'vendedores sin comillas'}
    return render(request, 'vendedores.html')