#!/usr/bin/env python
#
#   dsb/services/urls.py
#   dsb
#

import re

from django.conf import settings
from django.conf.urls.defaults import *

__author__ = 'Ross Light'
__date__ = 'June 5, 2009'
__all__ = ['urlpatterns']

urlpatterns = patterns('',
)

if getattr(settings, 'GOOGLE_WEBMASTER_FILE', None):
    urlpatterns += patterns('dsb.services.views',
        url(r'^%s$' % re.escape(settings.GOOGLE_WEBMASTER_FILE),
            'webmaster', name='dsb.services.webmaster'),
    )
