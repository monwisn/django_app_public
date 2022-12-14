"""
Django settings for plants_app project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import environ

import dj_database_url
import django_heroku
import cloudinary
import cloudinary_storage

from pathlib import Path

from django.contrib import messages, staticfiles
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = True  # development
DEBUG = False  # production

ADMINS = (
    ('admin', 'YOUR_GMAIL'),
)

MANAGERS = ADMINS

# ALLOWED_HOSTS = ["*"]  # don't use it for production
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com', '.ngrok.io']

CSRF_TRUSTED_ORIGINS = ['https://*.ngrok.io', 'https://*.127.0.0.1', 'https://*.herokuapp.com']

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'dal',
    'dal_select2',
    'whitenoise.runserver_nostatic',  # above the built-in staticfiles
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_filters',
    'import_export',
    'crispy_forms',
    'ckeditor',
    'sorl.thumbnail',
    'rest_framework',
    'guardian',
    'translation_manager',
    'rosetta',
    'webpush',
    'cloudinary',
    'cloudinary_storage',

    'main.apps.MainConfig',
    'authentication.apps.AuthenticationConfig',
    'control_panel.apps.ControlPanelConfig',
    'blog.apps.BlogConfig',
    'galleries.apps.GalleriesConfig',
]

# LocaleMiddleware: # this middleware should come after the SessionMiddleware because it needs to use the session data.
# It should also be placed before the CommonMiddleware because the CommonMiddleware needs the active language to resolve
# the URLs being requested.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # add whitenoise exactly here
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # add exactly here
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'plants_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'plants_app.wsgi.application'

# postgres database:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': env("DATABASE_PORT"),
    }
}

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

# Database for Docker:

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ.get('POSTGRES_NAME'),
#         'USER': os.environ.get('POSTGRES_USER'),
#         'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "PUBLIC_KEY",
    "VAPID_PRIVATE_KEY": "PRIVATE_KEY",
    "VAPID_ADMIN_EMAIL": "YOUR_GMAIL"
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('pl', _('Polish')),
    ('es', _('Spanish')),
)

LOCALE_PATHS = [BASE_DIR / 'locale', ]

LANGUAGE_COOKIE_NAME = 'django_language'

LANGUAGE_SESSION_KEY = '_language'

# TRANSLATIONS_BASE_DIR = BASE_DIR

TRANSLATIONS_IGNORED_PATHS = ['env', ]

TRANSLATIONS_MAKE_BACKUPS = True

TRANSLATIONS_CLEAN_PO_AFTER_BACKUP = False

TRANSLATIONS_ADMIN_EXCLUDE_FIELDS = ['get_hint', 'locale_parent_dir', 'domain']

TRANSLATIONS_HINT_LANGUAGE = 'en'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'  # is the URL location of static files located in STATIC_ROOT
MEDIA_URL = '/media/'

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'main/static'), ]  # tells Django where to look for static files in a Django project

else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'main/static')   # the absolute path to the directory where collectstatic will collect static files for deployment

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# to reduce the size of the static files when they are served (more efficient)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


TEMPLATE_LOADERS = 'django.template.loaders.filesystem.Loader'

# To serve files directly from their original locations
WHITENOISE_USE_FINDERS = True

# Cloudinary to serve media files
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'NAME',
    'API_KEY': 'API_KEY',
    'API_SECRET': 'API_SECRET_KEY',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

SHELL_PLUS_PRINT_SQL = True

CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_URL = '/authentication'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

NEWSLETTER_THUMBNAIL = 'sorl-thumbnail'
NEWSLETTER_ROOT = BASE_DIR / 'main/templates'

# Gmail sending config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'YOUR_GMAIL'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'YOUR_GMAIL'
EMAIL_HOST_PASSWORD = 'GENERATED FOR THIRD-PARTY APPS PASSWORD'
EMAIL_PORT = 587  # this is gmail's port
EMAIL_USE_TLS = True  # this encrypts our emails being sent

# Django REST Framework:
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

# Django messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# To activate django-heroku
django_heroku.settings(locals())
