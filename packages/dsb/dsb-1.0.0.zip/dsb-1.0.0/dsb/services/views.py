#!/usr/bin/env python
#
#   dsb/services/views.py
#   dsb
#

from django.http import HttpResponse

__author__ = 'Ross Light'
__date__ = 'June 4, 2009'
__all__ = ['webmaster']

def webmaster(request):
    """Google Webmaster verification file"""
    return HttpResponse('')
