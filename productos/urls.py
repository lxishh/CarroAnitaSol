from django.urls import path
from . import views

urlpatterns = [
    path('listado/', views.listar_productos, name='productos'),
    path('registrar/', views.registrar_producto, name='registrarproducto'),
    path('actualizar/<int:id>', views.actualizar_producto, name='actualizarproducto'),
    path('eliminar/<int:id>', views.eliminar_producto, name='eliminarproducto'),
    path('registrar/categoria', views.registrar_categoria, name='registrarcategoria'),
    path('categorias/', views.listar_categorias, name='categorias'),
    path('categorias/actualizar/<int:id>/', views.actualizar_categoria, name='actualizarcategoria'),
    path('categorias/eliminar/<int:id>/', views.eliminar_categoria, name='eliminarcategoria'),
]