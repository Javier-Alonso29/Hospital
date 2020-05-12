from .models import Usuario
from django.contrib.auth.models import Permission

def total_permisos(request):
    queryset = [(x.name) for x in Permission.objects.all()]
    kwargs = {
        'total_permisos' : queryset
    }

    return kwargs