#!/usr/bin/env python
#
#   dsb/data/utils.py
#   dsb
#

"""Data functions"""

from base64 import b64encode, b64decode

from django.http import HttpResponse
from django.utils import simplejson
from django.utils.functional import lazy
from django.utils.translation import ugettext as _

__author__ = 'Ross Light'
__date__ = 'May 7, 2009'
__docformat__ = 'reStructuredText'
__all__ = [
    'json_response',
    'human_list',
    'to_uuid',
    'uuid2shortid',
    'shortid2uuid',
]

def json_response(data={}, status=200, callback=None, **kw):
    """
    Render a JSON response.
    
    Any additional keywords will be part of the data.
    
    :Parameters:
        data
            An object to be converted to JSON.  This will call `as_dict`
            internally.
    :Keywords:
        status : int
            The status code to return.
        callback : str
            The callback for a JSONP request.
    :Returns: The equivalent response
    :ReturnType: django.http.HttpResponse
    """
    from dsb.data.json import as_dict
    data = as_dict(data)
    data.update(as_dict(kw))
    result = simplejson.dumps(data, separators=(',', ':'))
    if callback:
        # JSONP
        result = '%s(%s)' % (callback, result)
    return HttpResponse(result, 'text/json', status)

def human_list(seq):
    """
    Transform a list of strings into a human-readable list.
    
    :Parameters:
        seq : iterable
            A sequence of strings
    :Returns: The human-readable list
    :ReturnType: unicode
    """
    seq = list(seq)
    if len(seq) == 0:
        return u''
    elif len(seq) == 1:
        return seq[0]
    elif len(seq) == 2:
        return _('%(1)s and %(2)s') % {'1': seq[0], '2': seq[1]}
    else:
        result = _(', ').join(seq[:-1])
        result = _('%(list)s, and %(final)s') % {
            'list': result, 'final': seq[-1]}
        return result

human_list = lazy(human_list, unicode)

def to_uuid(value):
    """
    Convert an object to a UUID.
    
    This can convert strings, integers, and lists into UUIDs.
    
    :Parameters:
        value
            A value to convert to a UUID
    :Raises TypeError: If the value could not be converted
    :Returns: The UUID equivalent of the value
    :ReturnType: uuid.UUID
    """
    from uuid import UUID
    if isinstance(value, UUID) or value is None:
        return value
    elif isinstance(value, basestring):
        if len(value) == 16:
            return UUID(bytes=value)
        else:
            return UUID(value)
    elif isinstance(value, (int, long)):
        return UUID(int=value)
    elif isinstance(value, (list, tuple)):
        return UUID(fields=value)
    else:
        raise TypeError("Unrecognized type for UUID, got '%s'" %
                        (type(value).__name__))

def uuid2shortid(uuid):
    """
    Convert a UUID into a short ID.
    
    :Parameters:
        uuid
            A UUID to convert
    :Returns: A Base64-encoded version of the UUID with padding stripped
    :ReturnType: str
    """
    return b64encode(to_uuid(uuid).bytes, '-_')[:-2]

def shortid2uuid(shortid):
    """
    Convert a short ID into a UUID.
    
    :Parameters:
        shortid
            A Base64-encoded version of a UUID
    :Returns: The equivalent UUID
    :ReturnType: UUID
    """
    if isinstance(shortid, unicode):
        shortid = shortid.encode('ascii')
    if len(shortid) == 22:
        # This short ID has implicit padding
        shortid += '=='
    if len(shortid) == 24:
        # Full length encoding
        return to_uuid(b64decode(shortid, '-_'))
    else:
        # Uh-oh, we have a non-bitstring short id.  This sounds bad.
        raise ValueError("Short ID is the wrong size")
