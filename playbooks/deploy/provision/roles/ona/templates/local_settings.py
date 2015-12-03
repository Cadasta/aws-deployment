# get most settings from staging_example.py (which in turn, imports from
# settings.py)
from onadata.settings.common import *  # noqa

# # # now override the settings which came from staging # # # #
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'onadata',
        'USER': 'onadata',
        'PASSWORD': 'onadata',
        'HOST': '{{ db_host }}',
        'OPTIONS': {
            # note: this option obsolete starting with django 1.6
            'autocommit': True,
        }
    }
}

DATABASE_ROUTERS = []  # turn off second database

# Make a unique unique key just for testing, and don't share it with anybody.
SECRET_KEY = '{{ ona_app_secret }}'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'rest_framework.permissions.DjangoModelPermissions'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'onadata.libs.authentication.DigestAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'onadata.libs.authentication.TempTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.UnicodeJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONPRenderer',
        'rest_framework.renderers.XMLRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ),
}
OAUTH2_PROVIDER['AUTHORIZATION_CODE_EXPIRE_SECONDS'] = 600
BROKER_TRANSPORT = 'librabbitmq'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    "{{ server_ip }}",
    "{{ ona_domain_name }}",
    "127.0.0.1"
]
CORS_ORIGIN_WHITELIST = (
    "{{ ona_domain_name }}",
    "{{ server_ip }}",
    'localhost:3000',
    'localhost:4000',
    'localhost:8000'
)

# Flags
TESTING_MODE = False

CORS_EXPOSE_HEADERS = (
    'Content-Type', 'Location', 'WWW-Authenticate', 'Content-Language',
)

MEDIA_URL = "{{ ona_survey_url }}/media/"
MEDIA_ROOT = '/var/ona/media/'

DEFAULT_FROM_EMAIL = 'info@{{ deployment_name }}-survey.cadasta.org'
