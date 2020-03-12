from django.urls import path
from .views import Login, Nuevo
from django.contrib.auth.views import LogoutView


app_name = 'usuarios'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('login/',logoutView.as_view(), name='logout'),
    path('nueo/',logoutView.as_view(), name='nuevo'),
]
