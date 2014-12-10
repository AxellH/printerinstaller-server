# Django settings for munkiwebadmin project.
import os
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

#######################################################
##  Configure printerinstaller server specific items ##
#######################################################

# Full Host name and port of server
# e.g http://127.0.0.1:8000
SERVER_HOST_NAME = "http://127.0.0.1:8000"

# Set this to true if you're running on Apache via wsgi module
RUNNING_ON_APACHE=False

# set this to True if you want to run on a subpath 
# the default path will be printers/
RUN_ON_SUBPATH=False

# Configuring Sparkle Updates
# if set to True you will be able to upload versions of Printer-Installer.app 
# and it will automatically create AppCasts for Sparkle, otherwise it will use the GITHUB_APPCAST_URL.
# If set to False it will use the appcast at the master github page, you can override this value below.
HOST_SPARKLE_UPDATES=True

# Set to true if you want to server PPD files
SERVE_FILES=True

# If not hosting sparkle updates, it will use this url for AppCasts.
# If building a custom version of Printer-Installer.app to provide a
# print quota software for your environment set this to your forks URL
GITHUB_APPCAST_URL="https://raw.githubusercontent.com/eahrold/Printer-Installer/master/Downloads/appcast.xml"

#################################################
##  End printerinstaller server specific items ##
#################################################

# Set this to the admins
ADMINS = (
    # ('My Admin', 'myadmin@work.com'),
)

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'printerinstaller.db'),
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                  
        'PORT': '',                
    }
}

MANAGERS = ADMINS
TEMPLATE_DEBUG = DEBUG

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

## Configure the subpath to run the Django App on
if RUN_ON_SUBPATH:
    SUB_PATH = 'printers/'
else:
    SUB_PATH=''

if HOST_SPARKLE_UPDATES:
    APPCAST_URL=os.path.join(SERVER_HOST_NAME,
                                        SUB_PATH,
                                        'sparkle/Printer-Installer/appcast.xml',
                                         )
else:
    APPCAST_URL=GITHUB_APPCAST_URL
    
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'files')

SPARKLE_PRIVATE_KEY_PATH=os.path.join(MEDIA_ROOT, 'private','dsa_priv.pem')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = SERVER_HOST_NAME + "/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
if RUNNING_ON_APACHE == True:
    STATIC_URL = '/static_printerinstaller/'
else:
    STATIC_URL = os.path.join('/',SUB_PATH,'static/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'site_static'),
)

LOGIN_URL=os.path.join('/',SUB_PATH,'login/')
LOGOUT_URL=os.path.join('/',SUB_PATH,'logout/')
LOGIN_REDIRECT_URL=os.path.join('/',SUB_PATH)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-wm9pil%hy8ww7vlwmc)0!473$7c2cx5q#046$8z$@gjxk+(zc'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'printerinstaller.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'printerinstaller.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'printerinstaller.context_processors.update_server',
    'django.contrib.auth.context_processors.auth'
    )


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.markup',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'printers',
    'south',
    'bootstrap_toolkit',
)

if HOST_SPARKLE_UPDATES and not 'DYNO' in os.environ :
    INSTALLED_APPS = INSTALLED_APPS + ('sparkle',)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

## Settings For deploying to heroku
if 'DYNO' in os.environ:
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']

    # Make Sure Debugging is false to Heroku
    DEBUG=False
    # If serving from heroku disable the ability to server files
    HOST_SPARKLE_UPDATES = False
    SERVE_FILES=False


