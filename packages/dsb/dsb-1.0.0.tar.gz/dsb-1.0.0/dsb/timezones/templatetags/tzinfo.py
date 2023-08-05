#!/usr/bin/env python
#
#   dsb/timezones/templatetags/tzinfo.py
#   zebracomic
#

"""Template filters for time zone manipulation"""

from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest

from dsb.timezones import utils

__author__ = 'Ross Light'
__date__ = 'June 5, 2009'
__all__ = ['utc', 'localtz']

register = template.Library()

def utc(value):
    """Convert a datetime to UTC."""
    return utils.to_utc(value)
register.filter('utc', utc)

def localtz(value, arg=None):
    """Convert a datetime to local time."""
    if isinstance(arg, User):
        timezone = utils.get_timezone(arg)
    elif isinstance(arg, HttpRequest):
        timezone = getattr(arg, 'timezone', utils.get_site_timezone())
    else:
        timezone = utils.get_site_timezone()
    return utils.to_local(value, timezone)
register.filter('localtz', localtz)
