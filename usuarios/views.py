from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from .forms import UsuarioForm
from .models import Usuario

class Login(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

class Nuevo(CreateView):
    template_name = 'nuevo.html'
    model = Usuario
    form_class = UsuarioFrom
