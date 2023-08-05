#!/usr/bin/env python
#
#   dsb/services/templatetags/analytics.py
#   dsb
#

"""Template tags for Google Analytics"""

from django import template
from django.conf import settings

__author__ = 'Ross Light'
__date__ = 'June 5, 2009'
__all__ = ['analytics']

register = template.Library()

def analytics():
    analytics_id = getattr(settings, 'GOOGLE_ANALYTICS_ID', '')
    if analytics_id.startswith('UA-'):
        analytics_id = analytics_id[3:]
    return {'GOOGLE_ANALYTICS_ID': analytics_id}
register.inclusion_tag('services/tags/analytics.html')(analytics)
