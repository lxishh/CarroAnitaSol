from django.urls import path
from . import views

urlpatterns = [
    path('listado/', views.listar_inventarios, name='inventario'),
    path('agregar/', views.registrar_inventario, name='registrarinventario'),
    path('actualizar/<int:id>', views.actualizar_inventario, name='actualizarinventario'),
    path('eliminar/<int:id>', views.eliminar_inventario, name='eliminarinventario'),
]