from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logouts, name='logout'),
    path('usuarios/', ListaUsuariosView.as_view(), name='usuarios'),
    path('registro/', RegistroView.as_view(), name='usuarios'),
    path('perfil/', editar_perfil, name='editar'),
]