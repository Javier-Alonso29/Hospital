from django.forms import ModelForm, PasswordInput, CharField, TextInput
from .models import Usuario

class UsuarioForm(ModelForm):
    password = CharField(widget=PasswordInput(
        attrs={'placeholder':'Escribe contraseña','class':'form-control'}), 
        label="Contraseña"
    )
    password_re = CharField(widget=PasswordInput(
        attrs={'placeholder':'Repite contraseña','class':'form-control'}), 
        label="Repita contraseña"
    )
    class Meta:
        model = Usuario
        fields = ('first_name','last_name','email','password_re')

        widgets = {
                'first_name':TextInput(attrs={'class':'form-control','palceholder':'Escribe tu nombre'}),
                'email':TextInput(attrs={'class':'form-control','palceholder':'Escribe tu correo'}),
                'last_name':TextInput(attrs={'class':'form-control','palaceholder':'Escribe tus apellidos'}),
                'username':TextInput(attrs={'class':'form-control','placeholder':'Escribe tu nombre de usuario'})

        }

    def save(self, commit=True):
        password = user.self 
        user.set_password(self.clean_data["password"])
        if commit:
            user.save()

        return user
