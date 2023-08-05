#!/usr/bin/env python
#
#   dsb/data/templatetags/humanlist.py
#   dsb
#

"""Template tags for making human-readable lists"""

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from dsb.data import utils

__author__ = 'Ross Light'
__date__ = 'June 5, 2009'
__all__ = ['humanlist', 'listfor']

register = template.Library()

def humanlist(value, autoescape=None):
    if autoescape:
        escape = conditional_escape
    else:
        escape = lambda s: s
    value = [escape(s) for s in value]
    return mark_safe(utils.human_list(value))
register.filter('humanlist', humanlist)
humanlist.needs_autoescape = True

class ListForNode(template.Node):
    def __init__(self, body, varname, iterator):
        self.body = body
        self.varname = varname
        self.iterator = template.Variable(iterator)
    
    def render(self, context):
        def subrender(value):
            context.push()
            context[self.varname] = value
            result = self.body.render(context).strip()
            context.pop()
            return result
        seq = self.iterator.resolve(context)
        return utils.human_list(subrender(value) for value in seq)

def listfor(parser, token):
    """
    Make a human-readable list.
    
    Example::
    
        {%listfor author in author_list%}
        <a href="{{author.get_absolute_url}}">{{author.name}}</a>
        {%endlistfor%}
    
    For authors John, Paul, and George, this will yield:
    
        <a href="#">John</a>, <a href="#">Paul</a>, and <a href="#">George</a>
    
    This is mainly used for linked lists.
    """
    # Parse arguments
    args = token.split_contents()[1:]
    if len(args) != 3 or args[1] != 'in':
        raise template.TemplateSyntaxError("listfor VAR in LIST")
    varname = args[0]
    iterator = args[2]
    # Parse body
    nodelist = parser.parse(('endlistfor',))
    parser.delete_first_token()
    # Create node
    return ListForNode(nodelist, varname, iterator)
register.tag('listfor', listfor)
