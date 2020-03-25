from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
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



class Login(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm


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

        return redirect('usuarios:login')
        



class Perfil(SuccessMessageMixin, UpdateView):
    template_name = 'perfil.html'
    model = Usuario
    form_class = PerfilForm
    success_message = "El usuario %(first_name)s se actualizó con éxito"


    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        url = reverse_lazy('usuarios:perfil', kwargs={'pk': pk})
        return url