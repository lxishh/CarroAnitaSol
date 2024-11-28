from django.urls import path
from . import views

urlpatterns = [
    path('listado/', views.listar_inventarios, name='inventarios'),
    path('inventario/agregar/', views.registrar_inventario, name='registrarinventario'),
]