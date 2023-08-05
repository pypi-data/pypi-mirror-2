#!/usr/bin/env python
#
#   dsb/data/json.py
#   dsb
#

"""
JSON serialization

Don't get me wrong, Django's system is great, but it adds cruft and doesn't
allow you to add non-column attributes to the output.  This module *does*.
"""

import datetime

from django.db import models
from django.utils import simplejson
from django.contrib.auth.models import User
from dsb.overloading import overloaded

__author__ = 'Ross Light'
__date__ = 'June 8, 2009'
__all__ = [
    'as_dict',
    'simple_dict',
]

@overloaded
def as_dict(value):
    """
    Convert a value to a dictionary suitable for JSON.
    
    :Parameters:
        value
            The value to convert
    :ReturnType: dict
    """
    obj_as_dict = getattr(value, 'as_dict', None)
    if obj_as_dict:
        return as_dict(obj_as_dict())
    else:
        raise TypeError("Don't know how to convert %r to a dictionary" %
            type(value).__name__)

# Simple values

@as_dict.register(str)
@as_dict.register(unicode)
@as_dict.register(int)
@as_dict.register(long)
@as_dict.register(float)
@as_dict.register(bool)
@as_dict.register(type(None))
def simple_as_dict(value):
    return value

@as_dict.register(tuple)
@as_dict.register(list)
def seq_as_dict(value):
    result = [as_dict(item) for item in value]
    return type(value)(result)

@as_dict.register(dict)
def dict_as_dict(obj):
    result = {}
    for key, value in obj.iteritems():
        result[key] = as_dict(value)
    return result

# Custom extensions

@as_dict.register(datetime.date)
@as_dict.register(datetime.time)
@as_dict.register(datetime.datetime)
def datetime_as_dict(value):
    return value.isoformat()

@as_dict.register(models.Model)
def model_as_dict(obj):
    obj_as_dict = getattr(obj, 'as_dict', None)
    result = {'__model__': str(obj._meta)}
    if obj_as_dict:
        # The model has a specific method!
        result.update(as_dict(obj_as_dict()))
        return result
    else:
        # Fallback on introspection
        fields = [name for name in obj._meta.get_all_field_names()
                  if not name.startswith('_')]
        result.update(simple_dict(fields, obj))
        return result

@as_dict.register(User)
def user_as_dict(user):
    result = simple_dict(('id', 'username'), user)
    result['__model__'] = 'auth.user'
    return result

def simple_dict(attr_list, obj):
    """
    Create a simple dictionary from an object.
    
    This will get all of the attributes requested from the object and then
    convert them with `as_dict`.
    
    :Parameters:
        attr_list : sequence of str
            The attributes to copy
        obj
            The object to copy from
    :Returns: The corresponding object
    :ReturnType: dict
    """
    result = {}
    for attr_name in attr_list:
        try:
            value = getattr(obj, attr_name)
        except AttributeError:
            pass
        else:
            result[attr_name] = as_dict(value)
    return result
