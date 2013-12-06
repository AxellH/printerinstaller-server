from django.core.exceptions import ValidationError

def validate_protocol(value):
    supported_protocols = ['ipp','http','socket','lpd','https'];
    if not value in supported_protocols:
        raise ValidationError(u'protocol %s is not currently supported' % value)