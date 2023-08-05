#!/usr/bin/env python
#
#   dsb/data/models.py
#   dsb
#

from django import forms
from django.conf import settings
from django.contrib.admindocs import views as admindocs_views
from django.db import backend, connection, models
from django.utils.translation import ugettext_lazy as _

from dsb.data.utils import to_uuid

__author__ = 'Ross Light'
__date__ = 'August 1, 2009'
__docformat__ = 'reStructuredText'
__all__ = [
    'UUIDField',
]

class UUIDField(models.Field):
    """
    A UUID database field.
    
    This field is only available on Python 2.5 and up (because of the
    dependency on the well-written ``uuid`` module).  This field also takes
    advantage of the `uuid type`_ in `PostgreSQL`_ 8.3 and above.  If your
    database does not support UUIDs, this field defaults to a 32-byte
    character string.
    
    .. _uuid type: http://www.postgresql.org/docs/8.3/static/datatype-uuid.html
    .. _PostgreSQL 8.3: http://www.postgresql.org/
    """
    
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kw):
        kw['blank'] = False
        kw['max_length'] = 32
        auto_generate = kw.pop('auto_generate', False)
        if auto_generate:
            kw['editable'] = False
        super(UUIDField, self).__init__(*args, **kw)
        self.auto_generate = auto_generate

    def db_type(self):
        if settings.DATABASE_ENGINE.startswith('postgresql'):
            if backend.get_version(connection.cursor()) >= (8, 3, 0):
                return 'uuid'
            else:
                return 'char(32)'
        else:
            return 'char(32)'

    def to_python(self, value):
        if not value:
            return None
        return to_uuid(value)

    def get_db_prep_value(self, value):
        if not value:
            return None
        return to_uuid(value).hex

    def pre_save(self, model_instance, add):
        from uuid import uuid4
        if add and self.auto_generate:
            setattr(model_instance, self.attname, uuid4())
        return getattr(model_instance, self.attname)

    def formfield(self, **kw):
        defaults = {'form_class': forms.CharField}
        defaults.update(kw)
        return super(UUIDField, self).formfield(**defaults)

admindocs_views.DATA_TYPE_MAPPING['UUIDField'] = _("Universally Unique ID")
