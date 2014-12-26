import os
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from urlparse import urlunparse
from urllib2 import quote
register = template.Library()

def _gen_url(site_info, value):
    scheme = site_info.get('scheme')
    host = site_info.get('host')
    path = quote(os.path.join(site_info.get('subpath'), value))
    return scheme, host, path

@register.filter(is_safe=True)
def pi_url(value, site_info):
    scheme, host, path = _gen_url(site_info, value)
    swap_scheme = 'printerinstallers' if scheme is 'https' else 'printerinstaller'
    return mark_safe(
        urlunparse([swap_scheme, host, path, None, None, None])
        )

@register.filter(is_safe=True)
def xml_url(value, site_info):
    scheme, host, path = _gen_url(site_info, value)
    return mark_safe(
        urlunparse([scheme, host, path, None, None, None])
        )
