from django.core.exceptions import ValidationError
from conf import supported_protocols
def validate_protocol(value):
    # supported_protocols = ['ipp','http','socket','lpd','https']
    # if not value in supported_protocols:
        #raise ValidationError(u'protocol %s is not currently supported' % value)
	is_supported = False

	for i in supported_protocols:
		if i[0] == value:
			is_supported = True
			break

	if not is_supported:
		raise ValidationError(u'protocol %s is not currently supported' % value)

def validate_printer_name(value):
	if " " in value:
		raise ValidationError(u'printer name can not contain spaces')
	if value[0].isdigit():
		raise ValidationError(u'printer name must start with letter')
