from django.urls import path
from .views import Login, Nuevo, Perfil, Lista, Permisos, addAdmin, deleteAdmin, addUser, deleteUser
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('nuevo/', Nuevo.as_view(), name='nuevo'),
    path('perfil/', Perfil.as_view(), name='perfil'),
    path('activar/<slug:uidb64>/<slug:token>', views.ActivarCuenta.as_view(), name ='activar'),
    path('lista/',Lista.as_view(), name='lista'),
    path('permisos/<int:pk>',Permisos.as_view(),name='permisos'),
    path('addAdministrador/<int:pk>',addAdmin, name='nadmin'),
    path('deleteAdministrador/<int:pk>',deleteAdmin,name='deleteAdmin'),
    path('addUsuario/<int:pk>',addUser,name='addUser'),
    path('deleteUsuario/<int:pk>',deleteUser,name='deleteUser'),
]
