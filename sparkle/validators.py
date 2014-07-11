from django.core.exceptions import ValidationError
from sparkle.conf import SUPPORTED_EXTENSIONS

def validate_private_key(file):
	if not file.name.endswith('.pem') or file is None:
		raise ValidationError(u'The file must be a .pem file')

	contents = file.readline().strip()
	if not contents == '-----BEGIN DSA PRIVATE KEY-----':
		raise ValidationError(u'%s is not a DSA private key file' % (file,))
	else:
		return True


