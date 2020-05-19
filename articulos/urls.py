from django.urls import path
from .views import Lista, comprar, confirmaCompra, cancelarCompra, VerCarrito, HistorialVenta
from . import views

app_name = 'articulos'

urlpatterns = [
    path('lista/', Lista.as_view(), name='lista'),
    path('comprar/', comprar, name='comprar'),
    path('vercarrito/',VerCarrito.as_view(),name='vercarrito'),
    path('confirmaCompra/<int:pk>',confirmaCompra,name='confirmaCompra'),
    path('cancelarCompra/',cancelarCompra, name='cancelarCompra'),
    path('historialVentas', HistorialVenta.as_view(), name='historialVenta'),
]
