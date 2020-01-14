from django import template
from django.template.base import Node
from django.templatetags.static import do_static

register = template.Library()


class AbsoluteStaticNode(Node):
    def __init__(self, path):
        self._path = path

    def render(self, context):
        url = self._path.render(context)
        return context.request.build_absolute_uri(url)


@register.tag
def absolute_static(parser, token):
    return AbsoluteStaticNode(do_static(parser, token))
