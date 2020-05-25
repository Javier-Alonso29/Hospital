from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, AccessMixin
from django.views.generic.list import ListView
from django.views.generic import TemplateView, DeleteView
from .models import Articulo, Venta, DetalleVenta
from usuarios.models import Usuario
from django import template
from django.urls import reverse_lazy
from datetime import datetime
from django.contrib import messages


class Lista(LoginRequiredMixin,ListView):
    model = Articulo
    paginate_by = 6

def comprar(request):

    pk = request.POST.get('id')
    cantidad = int(request.POST.get('cantidad'))

    articulo = get_object_or_404(Articulo, pk=pk)
    
    if articulo.stock > 0:

        #articulo.stock = articulo.stock - cantidad

        articulo.save()

        id = str(pk)
        request.session['total'] = request.session['total'] + float(articulo.precio) * cantidad
        request.session['cuantos'] = request.session['cuantos'] + cantidad

        if( id in request.session['articulos']):
            request.session['articulos'][id]['cantidad'] = request.session['articulos'][id]['cantidad'] + cantidad
        else:
            request.session['articulos'][id] = {'nombre':articulo.nombre,'precio':float(articulo.precio),'cantidad': cantidad,}

            print(request.session['articulos'])

    return redirect('articulos:lista')


class VerCarrito(LoginRequiredMixin,ListView):
    model = Articulo
    template_name = 'articulos/venta_list.html'

    def get_queryset(self):

        id_articulos = list(self.request.session['articulos'].keys())

        carrito = list()

        for id in id_articulos:
            articulo = Articulo.objects.get(pk = id)
            cantidad = self.request.session['articulos'][id]['cantidad']

            tempo = (articulo,cantidad)
            print(tempo)

            carrito.append(tempo)
            

        return carrito

def confirmaCompra(request, pk):

    id_articulos = list(request.session.get('articulos').keys())

    print(id_articulos)
    print(Usuario.objects.get( pk = pk))

    venta = Venta.objects.create(fecha = datetime.now() , usuario = Usuario.objects.get( pk = pk))
    venta.save()


    for id in id_articulos:

        articulo = Articulo.objects.get(pk = id)
        cantidad = request.session['articulos'][id]['cantidad']
        articulo.stock = articulo.stock - cantidad
        articulo.save()

        #detalle = DetalleVenta(articulo.id, venta.id)
        detalle = DetalleVenta.objects.create(articulo = articulo, venta = venta)

        detalle.save()

        
    messages.success(request, 'Felicidades por tu compra!!')
    
    request.session['articulos'] = {}
    request.session['total'] = 0
    request.session['cuantos'] = 0  

    
    return redirect('articulos:lista')


def cancelarCompra(request):
    
    request.session['articulos'] = {}
    request.session['total'] = 0
    request.session['cuantos'] = 0  

    messages.error(request, 'Tu compra ha sido cancelada')

    return redirect('articulos:lista')


class HistorialVenta(LoginRequiredMixin,ListView):
    model = DetalleVenta


def eliminar(request, pk):
    val = int(pk)
    obj = get_object_or_404(Articulo, id = val)
    print(obj)
    obj.delete()
    return redirect('articulos:lista')