#!/usr/bin/env python
#
#   dsb/links/decorators.py
#   dsb
#

"""Various link decorators"""

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import functional

__author__ = 'Ross Light'
__date__ = 'June 4, 2009'
__docformat__ = 'reStructuredText'
__all__ = ['secure_page']

def secure_page(func):
    """
    Ensure that a page is viewed securely.
    
    This only attempts to redirect the user if the ``ALLOW_HTTPS`` setting is
    ``True``.
    
    :Parameters:
        func : callable
            The view function to secure
    :ReturnType: callable
    """
    def _wrapper(request, *args, **kw):
        if getattr(settings, 'ALLOW_HTTPS', False) and not request.is_secure():
            host, path = request.get_host(), request.get_full_path()
            url = 'https://' + host + path
            return HttpResponseRedirect(url)
        else:
            return func(request, *args, **kw)
    functional.update_wrapper(_wrapper, func)
    return _wrapper
