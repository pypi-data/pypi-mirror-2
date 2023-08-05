#!/usr/bin/env python
#
#   dsb/timezones/models.py
#   dsb
#

from datetime import tzinfo

from django.db import models
from django.utils.translation import ugettext_lazy as _
import pytz

__author__ = 'Ross Light'
__date__ = 'June 7, 2009'
__all__ = [
    'TimezoneField',
]

class TimezoneField(models.Field):
    """
    A field that stores a ``pytz`` timezone.
    """
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, **kw):
        kw.setdefault('max_length', 32)
        super(TimezoneField, self).__init__(**kw)
    
    def db_type(self):
        return 'VARCHAR(%i)' % (self.max_length)
    
    def to_python(self, value):
        if isinstance(value, tzinfo):
            return value
        elif value:
            return pytz.timezone(value)
        else:
            return None
    
    def get_db_prep_value(self, value):
        if isinstance(value, tzinfo):
            return value.zone
        else:
            return value
    
    def get_internal_type(self):
        return 'TimezoneField'
    
    def formfield(self, **kw):
        from django import forms
        params = {
            'form_class': forms.ChoiceField,
            'choices': [(tz, _(tz)) for tz in pytz.common_timezones],
        }
        params.update(kw)
        return super(TimezoneField, self).formfield(**params)
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

# Add field name to admin docs
from django.contrib.admindocs import views as docs_views
docs_views.DATA_TYPE_MAPPING['TimezoneField'] = _("Timezone")
