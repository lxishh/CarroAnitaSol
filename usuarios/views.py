from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menuopciones')
         # Redirect to a success page.
        else:
            messages.success(request, 'Error al iniciar sesión, vuelva a intentarlo.')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html')
    
def logout_usuario(request):
    logout(request)
    messages.success(request, 'Sesion cerrada con éxito')
    return redirect("home")