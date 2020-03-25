from .models import Paciente

def pacientes_contador(request):
    kwargs = {
        'contador': Paciente.objects.all().count() 
    }
    return kwargs