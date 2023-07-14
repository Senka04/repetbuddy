from django import template
from transliterate import translit

register = template.Library()

@register.filter
def transliterate(value):
    return translit(value, 'ru', reversed=True)
