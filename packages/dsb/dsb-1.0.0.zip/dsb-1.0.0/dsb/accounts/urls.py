#!/usr/bin/env python
#
#   dsb/accounts/urls.py
#   dsb
#

from django.conf.urls.defaults import *

__author__ = 'Ross Light'
__date__ = 'June 4, 2009'
__all__ = ['urlpatterns']

urlpatterns = patterns('dsb.accounts.views',
    url(r'^login/$', 'login', name='dsb.accounts.login'),
    url(r'^autologin/$', 'login',
        {'template_name': 'registration/autologin.html'},
        name='dsb.accounts.autologin'),
    url(r'^logout/$', 'logout', name='dsb.accounts.logout'),
)
