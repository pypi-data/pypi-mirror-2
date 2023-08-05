#!/usr/bin/env python
#
#   dsb/accounts/middleware.py
#   dsb
#

from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.http import urlquote
from django.contrib.auth import REDIRECT_FIELD_NAME

__author__ = 'Ross Light'
__date__ = 'June 9, 2009'
__all__ = ['AutologinMiddleware']

class AutologinMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            path = urlquote(request.get_full_path())
            return HttpResponseRedirect('%s?%s=%s' %
                (settings.LOGIN_URL, REDIRECT_FIELD_NAME, path))
