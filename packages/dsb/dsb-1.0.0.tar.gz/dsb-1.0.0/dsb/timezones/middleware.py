#!/usr/bin/env python
#
#   dsb/timezones/middleware.py
#   dsb
#

from dsb.timezones.utils import get_timezone

__author__ = 'Ross Light'
__date__ = 'April 1, 2009'
__all__ = ['TimezoneMiddleware']

class TimezoneMiddleware(object):
    def process_request(self, request):
        user = getattr(request, 'user', None)
        request.timezone = get_timezone(user)
