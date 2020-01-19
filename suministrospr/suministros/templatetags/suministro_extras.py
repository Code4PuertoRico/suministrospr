from django import template
from django.templatetags.static import static
from django.utils.text import slugify

register = template.Library()


@register.simple_tag
def escudo_static(value):
    return static(f"img/escudos/{slugify(value)}.png")
