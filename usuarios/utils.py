from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def rol_requerido(rol_requerido):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'usuario') or request.user.usuario.rol != rol_requerido:
                return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
