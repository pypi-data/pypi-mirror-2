#!/usr/bin/env python
#
#   dsb/data/markup.py
#   dsb
#

"""Common markup language support"""

from django.utils import html
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

# Markdown import
try:
    import markdown
except ImportError:
    MARKDOWN_INSTALLED = False
else:
    MARKDOWN_INSTALLED = True

__author__ = 'Ross Light'
__date__ = 'August 16, 2009'
__docformat__ = 'reStructuredText'
__all__ = [
    'MARKDOWN_INSTALLED',
    'UnknownFormatError',
    'FormatNotInstalledError',
    'render_markup',
    'MARKUP_LIST',
]

class UnknownFormatError(Exception):
    """Raised when an unknown markup format is specified"""

class FormatNotInstalledError(Exception):
    """Raised when a markup format is """

def render_markup(source, format='html', options=None):
    """
    Convert markup into HTML.
    
    :Parameters:
        source : unicode
            The source markup
        format : str
            The markup language of the source.  Must be one of the choices in
            `MARKUP_LIST`.
        options : dict
            Options for the markup language.
    :Raises AssertionError: If the format is not in `MARKUP_LIST`
    :Returns: Equivalent HTML markup (marked as safe)
    :ReturnType: unicode
    """
    # Default options
    if options is None:
        options = {}
    # Get render function
    try:
        render_func = _markup_funcs[format]
    except KeyError:
        raise UnknownFormatError("%r is not a recognized format" % (format))
    # Render the markup
    return render_func(source, options)

def _render_markdown(source, options):
    # We may not have Markdown installed
    if not MARKDOWN_INSTALLED:
        raise FormatNotInstalledError("Markdown not installed")
    # Get options
    safe_mode = options.get('safe_mode', True)
    extensions = options.get('extensions', [])
    # Markdown rendering
    if getattr(markdown, 'version', None):
        if getattr(markdown, 'version_info', None) < (1, 7):
            # Pre-1.7
            return mark_safe(force_unicode(markdown.markdown(
                smart_str(source),
                extensions, safe_mode=safe_mode)))
        else:
            # 1.7 or later
            return mark_safe(markdown.markdown(
                force_unicode(source),
                extensions, safe_mode=safe_mode))
    else:
        # 1.6.2rc-2 or before
        return mark_safe(force_unicode(markdown.markdown(
            smart_str(source))))

def _render_html(source, options):
    return mark_safe(source)

def _render_plain(source, options):
    return mark_safe(html.linebreaks(html.escape(source)))

_markup_info = (
    ('markdown',    _render_markdown,   _("Markdown")),
    ('html',        _render_html,       _("HTML")),
    ('plain',       _render_plain,      _("Plain text")),
)
_markup_funcs = dict((key, func) for (key, func, name) in _markup_info)
MARKUP_LIST = tuple((key, name) for (key, func, name) in _markup_info)
