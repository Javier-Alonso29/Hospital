from django.urls import path
from .views import Lista, Nuevo, Eliminar, Editar, buscar_municipio,ListaPdf,Grafica

app_name = 'pacientes'

urlpatterns = [
    path('lista/', Lista.as_view(), name='lista'),
    path('nuevo/', Nuevo.as_view(), name='nuevo'),
    path('editar/<int:pk>', Editar.as_view(), name='editar'),
    path('eliminar/<int:pk>', Eliminar.as_view(), name='eliminar'),
    path('busca-municipio/', buscar_municipio, name='buscar_municipio'),
    path('pdf/', ListaPdf.as_view(), name='pdf'),
    path('graficas/', Grafica.as_view(), name='pacientes_graficas'),
]
