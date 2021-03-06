from .base import *
try:
    from .secret_key import *
except ImportError:
    SETTINGS_DIR=os.path.abspath(os.path.dirname(__file__))
    generate_secret_key(os.path.join(SETTINGS_DIR, 'secret_key.py'))
    from .secret_key import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = False

# Email
EMAIL_SUBJECT_PREFIX = '[KnoAtom] '
SERVER_EMAIL = 'knoatom-noreply@umich.edu'

#smtp
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'knoatom.webmaster@gmail.com'
EMAIL_HOST_PASSWORD = 'djangogrubsalad'
EMAIL_PORT = 587

ALLOWED_HOSTS = [
    'localhost',
    'knoatom.eecs.umich.edu',
    'cportal-nt.eecs.umich.edu',
    '127.0.0.1',
    '141.213.4.210'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'knoatom',                      # Or path to database file if using sqlite3.
        'USER': 'knoatom_web',                      # Not used with sqlite3.
        'PASSWORD': 'uDKyrVX0Lb',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
PROJECT_ROOT = '/var/www/knoatom-web/'
# Function to turn relative paths from the project root into absolute paths

MEDIA_ROOT = '/var/www/knoatom-static/media/'
#MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/').replace('\\','/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/knoatom-static/static/'
#STATIC_ROOT = '/var/www/knoatom-static/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Make this unique, and don't share it with anybody.