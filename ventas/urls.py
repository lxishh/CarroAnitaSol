from django.urls import path
from . import views

urlpatterns = [
    path('listado/', views.listar_ventas, name='ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'),
    path('ventas/<int:pk>/', views.ver_venta, name='ver_venta'),
    path('ventas/<int:pk>/editar/', views.actualizar_venta, name='actualizar_venta'),
    path('ventas/<int:pk>/eliminar/', views.eliminar_venta, name='eliminar_venta'),
]
