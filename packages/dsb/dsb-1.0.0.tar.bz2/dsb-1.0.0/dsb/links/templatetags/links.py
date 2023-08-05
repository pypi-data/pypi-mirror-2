#!/usr/bin/env python
#
#   dsb/links/templatetags/links.py
#   dsb
#

"""Template tags for site URLs"""

from urlparse import urljoin

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.template import defaulttags

__author__ = 'Ross Light'
__date__ = 'June 4, 2009'
__all__ = ['static_url',
           'secure_url',]

register = template.Library()

class StaticURLNode(template.Node):
    def __init__(self, path, varname=None):
        self.path = path
        self.varname = varname
    
    def render(self, context):
        resource_url = urljoin(settings.STATIC_URL, self.path)
        if self.varname is None:
            return resource_url
        else:
            context[self.varname] = resource_url
            return ''

class SecureURLNode(defaulttags.URLNode):
    def render(self, context):
        # Do default rendering
        path = super(SecureURLNode, self).render(context)
        if self.asvar:
            path = context[self.asvar]
        # Compute full secure URL
        current_domain = Site.objects.get_current().domain
        url = 'https://' + current_domain + path
        # Render
        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url

def static_url(parser, token):
    args = token.split_contents()[1:]
    # Parse path
    if len(args) >= 1:
        path = args[0]
        if path[0] == path[-1] and path[0] in ("'", '"'):
            path = path[1:-1]
    # Create our node
    if len(args) == 1:
        return StaticURLNode(path)
    elif len(args) == 3 and args[1] == 'as':
        return StaticURLNode(path, args[2])
    else:
        raise template.TemplateSyntaxError("static_url URL [as VAR]")
register.tag('static_url', static_url)

def secure_url(parser, token):
    default_node = defaulttags.url(parser, token)
    if settings.ALLOW_HTTPS:
        return SecureURLNode(default_node.view_name, default_node.args,
                             default_node.kwargs, default_node.asvar)
    else:
        return default_node
register.tag('secure_url', secure_url)
