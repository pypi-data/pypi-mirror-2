#!/usr/bin/env python
#
#   dsb/data/views.py
#   dsb
#

from django.http import Http404
from django.core import serializers
from django.core.xheaders import populate_xheaders
from django.core.exceptions import ObjectDoesNotExist

from dsb.data.utils import json_response
from dsb.data.json import as_dict, simple_dict

__author__ = 'Ross Light'
__date__ = 'June 7, 2009'
__all__ = ['json_detail']

def json_detail(request, queryset,
                object_id=None, slug=None, slug_field='slug',
                fields=None):
    # Build query
    model = queryset.model
    if object_id:
        queryset = queryset.filter(pk=object_id)
    elif slug and slug_field:
        queryset = queryset.filter(**{slug_field: slug})
    else:
        raise AttributeError("Generic view must be called with either an object_id or a slug/slug_field.")
    # Get object
    try:
        obj = queryset.get()
    except ObjectDoesNotExist:
        raise Http404("No %s found matching the query" %
            model._meta.verbose_name)
    # Serialize
    if fields is None:
        result = as_dict(obj)
    else:
        result = {'__model__': str(obj._meta)}
        result.update(simple_dict(fields, obj))
    # Render
    response = json_response(result, callback=request.GET.get('callback'))
    populate_xheaders(request, response, model, getattr(obj, obj._meta.pk.name))
    return response
