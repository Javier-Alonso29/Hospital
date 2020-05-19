from django.template import Library
from django.template.defaulttags import register

register = Library()

@register.filter
def product_name(dictionary, key):
    return dictionary.get(key)