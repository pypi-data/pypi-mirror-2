# Django settings for demoproject project.

# DEMOPROJECT NOTE: I made minimum number of changes from default
# settings.py to have a basic demoproject. Changes are accompanied by
# comments that start with a big fat DEMOPROJECT NOTE marker

# DEMOPROJECT NOTE: Best practice to create a 'ROOT_DIR'. See usage below.
import os.path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# DEMOPROJECT NOTE: Added dev db
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
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

# DEMOPROJECT NOTE: (Absolute) Path to media
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

# DEMOPROJECT NOTE: Some paths to images are hardcoded to /media/ in
# css. There is no good way to handle this nicely. Or perhaps
# django-staticfiles. Need to look into that.
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".

# DEMOPROJECT NOTE: Some paths to images are hardcoded to
# /media/admin/ in css :-(
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '02g4h-y1x=g(m1b60qr@j41-hzz6&1%s^4aseqe8ghsdsr27a='

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
    # DEMOPROJECT NOTE: Added flatpages and contentmanager middleware
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'contentmanager.middleware.EditmodeMiddleware',
)

ROOT_URLCONF = 'demoproject.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    # DEMOPROJECT NOTE: Added templates dir
    os.path.join(ROOT_DIR, 'templates')
)

# DEMOPROJECT NOTE: Added this for the request context_processors which the contentmanager relies on
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request"
    )

# DEMOPROJECT NOTE: Added admin, flatpages, contentmanager,
# basicblocks, webdesign
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.webdesign',
    'contentmanager',
    'basicblocks',
)
