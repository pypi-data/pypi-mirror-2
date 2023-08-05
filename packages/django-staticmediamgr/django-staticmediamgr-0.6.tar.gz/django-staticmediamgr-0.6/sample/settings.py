# Django settings for sample project.
import os, sys

APP = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(APP)

APPS = os.path.join(os.path.dirname(__file__),'apps')
sys.path.append(APPS)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dev.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = APP + '/sample/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bwq#m)-zsey-fs)0#4*o=2z(v5g!ei=zytl9t-1hesh4b&-u^d'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'sample.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'staticmediamgr',
    'app1',
    'app2',
    'app3',
)

STATIC_MEDIA_COPY_PATHS = (
    {'from': os.path.join(APP, 'sample','media2'), 'to':os.path.join(APP, 'media2')},
    {'from': MEDIA_ROOT, 'to':os.path.join(APP, 'media2')},
)
STATIC_ROOT= os.path.join(APP, 'media2')
STATIC_URL = '/media/'
STATIC_MEDIA_APP_MEDIA_PATH = os.path.join(APP, 'media2')
STATIC_MEDIA_COMPRESS_JS = True
STATIC_MEDIA_COMPRESS_CSS = True
STATIC_MEDIA_PURGE_OLD_FILES = False

STATIC_MEDIA_FILE_COMBINATIONS = {
    MEDIA_ROOT+'/css/combo.css': [
        MEDIA_ROOT+'/css/base.css', 
        MEDIA_ROOT+'/css/forms.css', 
        MEDIA_ROOT+'/css/coolui.css'],
}

# STATIC_MEDIA_JS_COMPRESSION_CMD = 'java -jar ~/compiler-latest/compiler.jar --js %(infile)s --js_output_file %(outfile)s'