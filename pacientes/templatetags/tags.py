from django.template import Library
from django.template.defaulttags import register

register = Library()

@register.filter
def product_name(dictionary, key):
    articulo = dictionary.get(key)
    nombre = articulo.get('nombre')
    return nombre

@register.filter
def product_cantid(dictionary, key):
    articulo = dictionary.get(key)
    cantidad = articulo.get('cantidad')
    return cantidad