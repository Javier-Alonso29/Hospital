from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group, Permission
from .forms import UsuarioForm, PerfilForm
from .models import Usuario
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .token import token_activacion
from django.core.mail import send_mail
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, AccessMixin
from django.views.generic.list import ListView
from django.contrib import messages



class Login(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm


class Lista(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = 'usuarios.permiso_gestion_permisos'
    model = Usuario
    template_name = 'usuario_list.html'
    
    def has_group(usuario,nombre_grupo):
        return usuario.groups.filter(name=nombre_grupo).exists() 

def addAdmin(request, *args, **kwargs):
    id_user = kwargs['pk']
    usr = Usuario.objects.get(pk = id_user)
    grupos = usr.groups.all()
    print(grupos)


    if grupos.filter(name='administradores').exists():
        messages.error(request, 'El usuario {} ya existe en el grupo administradores'.format(usr.username))
    else:
        usr.groups.add(Group.objects.get(id=10))
        messages.success(request, 'El usuario {} se agrego a el grupo de administradores'.format(usr.username))
        
    return redirect('usuarios:lista')


def deleteAdmin(request, *args, **kwargs):
    id_user = kwargs['pk']
    usr = Usuario.objects.get(pk = id_user)
    grupos = usr.groups.all()
    print(grupos)


    if grupos.filter(name='administradores').exists():

        if(len(grupos)) == 1:
            messages.error(request,'El usuario {} debe de pertenecer al menos a un grupo'.format(usr.username))
        else:
            usr.groups.remove(Group.objects.get(id=10))
            messages.success(request,'Se elimino {} el usuario del grupo'.format(usr.username))
    else:
        messages.error(request,'El usuario {} no esta en el grupo de administracion'.format(usr.username))
    return redirect('usuarios:lista')

def addUser(request, *args, **kwargs):
    id_user = kwargs['pk']
    usr = Usuario.objects.get(pk = id_user)
    grupos = usr.groups.all()
    print(grupos)


    if grupos.filter(name='usuarios').exists():
        messages.error(request, 'El usuario {} ya existe en el grupo usuarios'.format(usr.username))
    else:
        usr.groups.add(Group.objects.get(id=12))
        messages.success(request, 'El usuario {} se agrego a el grupo de usuarios'.format(usr.username))
        
    return redirect('usuarios:lista')


def deleteUser(request, *args, **kwargs):
    id_user = kwargs['pk']
    usr = Usuario.objects.get(pk = id_user)
    grupos = usr.groups.all()
    print(grupos)

    if grupos.filter(name='usuarios').exists():

        if(len(grupos)) == 1:
            messages.error(request,'El usuario {} debe de pertenecer al menos a un grupo'.format(usr.username))
        else:
            usr.groups.remove(Group.objects.get(id=12))
            messages.success(request,'Se elimino {} el usuario del grupo usuarios'.format(usr.username))
    else:
        messages.error(request,'El usuario {} no esta en el grupo de usuarios'.format(usr.username))
    return redirect('usuarios:lista')

class Nuevo(CreateView):
    template_name = 'nuevo.html'
    model = Usuario
    form_class = UsuarioForm
    

    def form_valid(self, form):

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        dominio = get_current_site(self.request)
        mensaje = render_to_string('confirmar_cuenta.html',
            {
                'user': user,
                'dominio': dominio,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': token_activacion.make_token(user)
            }
        )

        email = EmailMessage(
            'Hospital mata sanos | Activa cuenta',
            mensaje,
            to=[user.email]
        )
        email.content_subtype = "html"
        email.send()
        mensaje = 'Verifica tu cuenta en tu correo electronico'
        return render(self.request,'login.html', {'mensaje':mensaje})
    #success_url = reverse_lazy('usuarios:login')
        

class ActivarCuenta(TemplateView):
    
    def get(self, request, *args, **kwargs):
        #context = self.get_context_data(**kwargs)
        try:
            uid = urlsafe_base64_decode(force_text(kwargs['uidb64']))
            token = kwargs['token']
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, User.DoesNotExist):
            user = None
        
        if user is not None and token_activacion.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(self.request, 'Cuenta activada, ingresa datos')
        else:
            messages.error(self.request, 'Token invalido, contacta con el administrador')

        return redirect('usuarios:lista')
        



class Perfil(SuccessMessageMixin, UpdateView):
    template_name = 'perfil.html'
    model = Usuario
    form_class = PerfilForm
    success_message = "El usuario %(first_name)s se actualizó con éxito"
    success_url = reverse_lazy('usuarios:perfil')

    def get_object(self, queryset=None):
        pk = self.request.user.pk
        obj = Usuario.objects.get(pk = pk)
        return obj

    """def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        url = reverse_lazy('usuarios:perfil', kwargs={'pk': pk})
        return url"""

class Permisos(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = 'usuarios.permiso_gestion_permisos'
    model = Usuario
    template_name = 'permisos.html'
    success_url = reverse_lazy('usuarios:lista')

    
    def get_queryset(self, **kwargs):
        pk = self.kwargs.get('pk',None)
        usr = Usuario.objects.get( id = pk)
        queryset = [(x.name) for x in Permission.objects.filter(user=usr)]
        print(queryset)
        return queryset
    

    