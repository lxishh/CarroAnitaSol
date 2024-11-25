from django.urls import path
from . import views

urlpatterns = [
    path('login_usuario', views.login_usuario, name='login'),
    path('logout_usuario', views.logout_usuario, name='logout'),
]