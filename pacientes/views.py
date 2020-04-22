from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Paciente, Municipio, Estado
from .forms import PacienteForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django_weasyprint import WeasyTemplateResponseMixin
from django.conf import settings
from django.views.generic import TemplateView
from django.db.models import Count
from datetime import date


class Lista(ListView):
    paginate_by = 5
    model = Paciente


class Nuevo(CreateView):
    model = Paciente
    form_class = PacienteForm
    
    success_url = reverse_lazy('pacientes:lista')

class Editar(UpdateView):
    model = Paciente
    form_class = PacienteForm
    extra_context = {'editar':True}

    success_url = reverse_lazy('pacientes:lista')

class Eliminar(DeleteView):
    model = Paciente
    success_url = reverse_lazy('pacientes:lista')


def buscar_municipio(request):
    id_estado = request.POST.get('id',None)
    if id_estado:
        municipios = Municipio.objects.filter(estado_id=id_estado)
        data = [{'id':mun.id,'nombre':mun.nombre} for mun in  municipios]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error':'Parámetro inválido'}, safe=False)


class VistaPdf(ListView):
    model = Paciente
    template_name = 'pacientes/paciente_pdf.html'
    
class ListaPdf(WeasyTemplateResponseMixin, VistaPdf):
    passpdf_stylesheets = [ settings.STATICFILES_DIRS[0] + 'dist/css/misEstilos.css']
    pdf_attachment = False
    pdf_filename = 'Pacientes.pdf'

class VistaPdfPaciente(ListView):
    model = Paciente
    template_name = 'pacientes/paciente_pdf_individual.html'

    def get_queryset(self, **kwargs):
        pk = self.kwargs.get('pk',None)
        queryset = Paciente.objects.filter( id = pk)
        return queryset
    

class PacientePdf(WeasyTemplateResponseMixin,VistaPdfPaciente):
    passpdf_stylesheets = [ settings.STATICFILES_DIRS[0] + 'dist/css/misEstilos.css' ]
    pdf_attachment = False
    pdf_filname = 'Paciente.pdf'


class Grafica(TemplateView):
    template_name = 'pacientes/grafica.html'
    pacientes_tipo = Paciente.objects.all().values('tipo_sangre').annotate(cuantos=Count('tipo_sangre'))
    tipos = Paciente.objects.all()

    datos = []
    tipos_de_sangre = []
    cuantos=0
    for tipo in tipos:
        if tipo.tipo_sangre in tipos_de_sangre:
            pass
        else:
            tipos_de_sangre.append(tipo.tipo_sangre)
            pt=pacientes_tipo[cuantos]
            num=pt['cuantos']
            datos.append({'name':tipo.tipo_sangre, 'data':[num]})
        cuantos=cuantos+1

    datos2 = []
    hoy = date.today()
    edades = Paciente.objects.all()
    edades_existentes = []
    ninos1=0
    ninos2=0
    ninos3=0
    adoles=0
    jovenes=0
    adultos1=0
    adultos2=0

    for edad in edades:
        año_paciente=edad.fecha_nac
        fecha=hoy.year - año_paciente.year - ((hoy.month, hoy.day) < (año_paciente.month, año_paciente.day))
        if fecha <= 3:
            ninos1=ninos1+1
        if fecha>3 and fecha<=7:
            ninos2=ninos2+1
        if fecha>7 and fecha<=12:
            ninos3=ninos3+1
        if fecha>12 and fecha<=17:
            adoles=adoles+1
        if fecha>17 and fecha<=29:
            jovenes=jovenes+1
        if fecha>29 and fecha<=49:
            adultos1=adultos1+1
        if fecha>=50:
            adultos2=adultos2+1

    datos2.append({'name':'niños 0-3 años', 'data':[ninos1]})
    datos2.append({'name':'niños 4-7 años', 'data':[ninos2]})
    datos2.append({'name':'niños 8-12 años', 'data':[ninos3]})
    datos2.append({'name':'adolescentes 13-17 años', 'data':[adoles]})
    datos2.append({'name':'jovenes 18-29 años', 'data':[jovenes]})
    datos2.append({'name':'adultos 30-49 años', 'data':[adultos1]})
    datos2.append({'name':'adultos 50 años o más', 'data':[adultos2]})
    extra_context = {'datos':datos,'datos2':datos2}
