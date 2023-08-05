#!/usr/bin/env python
#
#   dsb/timezones/utils.py
#   dsb
#

"""
Timezone calculations

All date calculations assume that naive datetimes are UTC.
"""

from datetime import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import SiteProfileNotAvailable
import pytz

__author__ = 'Ross Light'
__date__ = 'April 1, 2009'
__all__ = [
    'now',
    'local_now',
    'to_utc',
    'to_local',
    'datetime2db',
    'get_timezone',
]

def now():
    """
    Get the current UTC time.
    
    :Returns: Timezone-aware current time
    :ReturnType: datetime.datetime
    """
    return pytz.utc.localize(datetime.utcnow())

def local_now(timezone=None):
    """
    Get the current local time.
    
    :Parameters:
        timezone : datetime.tzinfo
            The local timezone
    :Returns: Timezone-aware current time
    :ReturnType: datetime.datetime
    """
    return to_local(now(), timezone)

def to_utc(dt):
    """
    Convert a datetime to UTC.
    
    :Parameters:
        dt : datetime.datetime
            The datetime to convert
    :Returns: The UTC equivalent
    :ReturnType: datetime.datetime
    """
    if dt.tzinfo is None:
        # Naive datetime
        return pytz.utc.localize(dt)
    else:
        # Convert to time zone
        return dt.astimezone(pytz.utc)

def to_local(dt, timezone=None):
    """
    Convert a datetime to local time.
    
    If no time zone is given, then the ``SITE_TIME_ZONE`` setting is used.
    
    :Parameters:
        dt : datetime.datetime
            The datetime to convert
        timezone : tzinfo or str
            The time zone, or the name of a time zone
    :Returns: The local equivalent
    :ReturnType: datetime.datetime
    """
    # Determine local time zone
    if timezone is None:
        timezone = get_site_timezone()
    elif isinstance(timezone, basestring):
        timezone = pytz.timezone(timezone)
    # Convert
    return to_utc(dt).astimezone(timezone)

def datetime2db(dt):
    """
    Convert a datetime to naive UTC datetime.
    
    :Parameters:
        dt : datetime.datetime
            The datetime to convert
    :Returns: A naive UTC datetime
    :ReturnType: datetime.datetime
    """
    return to_utc(dt).replace(tzinfo=None)

def get_timezone(user=None):
    """
    Determine the working time zone.
    
    :Parameters:
        user : django.contrib.auth.models.User
            If a user is given, then the function will try to use the user's
            time zone settings.
    """
    timezone = None
    # Attempt to get user settings
    if user is not None and user.is_authenticated():
        try:
            profile = user.get_profile()
        except (ObjectDoesNotExist, SiteProfileNotAvailable):
            pass
        else:
            timezone = getattr(profile, 'timezone', None)
    # If we don't have a time zone, get the site default
    if timezone is None:
        timezone = get_site_timezone()
    return timezone

def get_site_timezone():
    """
    Find the site's time zone.
    
    :Returns: The site's time zone
    :ReturnType: datetime.tzinfo
    """
    tz_name = getattr(settings, 'SITE_TIME_ZONE', settings.TIME_ZONE)
    try:
        return pytz.timezone(tz_name)
    except pytz.UnknownTimeZoneError:
        return pytz.utc
