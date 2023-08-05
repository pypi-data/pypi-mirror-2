#!/usr/bin/env python
#
#   dsb/accounts/views.py
#   dsb
#

from django.contrib.auth import views as auth_views

from dsb.links.decorators import secure_page

__author__ = 'Ross Light'
__date__ = 'June 4, 2009'
__all__ = ['login', 'logout']

login = secure_page(auth_views.login)
logout = secure_page(auth_views.logout)
