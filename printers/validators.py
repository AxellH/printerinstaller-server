'''Validators'''
from django.core.exceptions import ValidationError
from printers.conf import supported_protocols

def validate_protocol(value):
    '''Check that the printer uri is a supported type'''
    is_supported = False

    for protocol in supported_protocols():
        if protocol[0] == value:
            is_supported = True
            break

    if not is_supported:
        raise ValidationError(u'protocol %s is not currently supported' % value)

def validate_printer_name(value):
    '''Check that the printer name is safe'''
    if " " in value:
        raise ValidationError(u'printer name can not contain spaces')
    if value[0].isdigit():
        raise ValidationError(u'printer name must start with letter')
