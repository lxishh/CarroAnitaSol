from django.urls import path
from . import views

urlpatterns = [
    path('listado/', views.listar_vendedores, name='vendedores'),
    path('registrar/', views.crear_vendedor, name='registrarvendedor'),
    path('actualizar/<int:id>', views.actualizar_vendedor, name='actualizarvendedor'),
    path('eliminar/<int:id>', views.eliminar_vendedor, name='eliminarvendedor'),
]
