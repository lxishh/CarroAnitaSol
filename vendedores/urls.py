from django.urls import path
from . import views

urlpatterns = [
    path('listado/', views.listar_vendedores, name='vendedores'),
]
