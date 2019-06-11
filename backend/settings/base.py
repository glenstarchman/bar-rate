import os
import requests
import socket


HOST_NAME=socket.gethostname()
if HOST_NAME == 'bar-rate-prod':
    MODE = 'production'
    DEBUG = FalseOB
    SITE_URL = "https://bar-rate.com"
else:
    MODE = 'development'
    DEBUG = True
    SITE_URL = "http://localhost:8000"


SITE_NAME='stems'
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HASHID_FIELD_SALT="jkgu76t7lubo87i87t788rfrvjjkbtijkhjhh755b7t87tv7i7iRV@#%%*#8ybyut7v6ri"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2+$mkjghgiy86t7g9kh-ifhf6fgkjo98y9trv0^@(*@tq2!lzb-ub)j_&93(80+wdv%ae+9jf=y2==x'

# SECURITY WARNING: don't run with debug turned on in production!

SITE_ID = 1


ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'localhost:8000',
    '13.58.201.14',
    '13.58.201.14:8000',

]

IS_DEV = False

#try:
#    internal_ip = requests.get('http://instance-data/latest/meta-data/local-ipv4').text
#except requests.exceptions.ConnectionError:
#    IS_DEV = True
#    pass
#else:
#    ALLOWED_HOSTS.append(internal_ip)
#del requests

#REMOVE THIS BEFORE GOING LIVE!!!!!!
#IS_DEV=True


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.postgres',
    'django.contrib.gis',
    'django.contrib.sites',
    'django_extensions',
    'rest_framework',
    'rest_framework_serializer_extensions',
    'rest_framework_swagger',
    'storages',
    # 'djstripe',
    'django_celery_results',
    'corsheaders',
    'rest_framework_docs',
    'api',
    'rest_framework.authtoken',
    'dry_rest_permissions',
    'django.contrib.admin',
    'django.contrib.auth',
    #'django_elasticsearch_dsl',
    #'django_elasticsearch_dsl_drf',
    'account',
    #'django_rest_passwordreset',
    #'django_admin_listfilter_dropdown',
]

#DATABASE_ROUTERS = ('api.db_router.StemsDBRouter',)

CELERY_RESULT_BACKEND = 'django-db'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'api.middleware.AddRequestTimestamp',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'public')],
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

WSGI_APPLICATION = 'wsgi.application'

AUTH_USER_MODEL = 'api.User'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'OPTIONS': {
                    'options': '-c search_path=public,stems,musicbrainz'
            },
        'NAME': 'bar_rate',
        'USER': 'bar_rate',
        'PASSWORD': 'bar_rate',
        'HOST': '127.0.0.1',
        'PORT': 5432
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api.util.Pagination',
    'PAGE_SIZE': 50,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'FORM_METHOD_OVERRIDE':
    None,
    'FORM_CONTENT_OVERRIDE':
    None,
    'FORM_CONTENTTYPE_OVERRIDE':
    None,
    'DEFAULT_VERSIONING_CLASS':
    'rest_framework.versioning.URLPathVersioning'
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SPECIAL_CHARS = '!~@#$%^&*()_+=_<>,./?'
NUMBERS = '1234567890'

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


CORS_ORIGIN_ALLOW_ALL = True

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", '')

DEFAULT_SEARCH_RADIUS = 50

#CITIES_FILES = {
#    'city': {
#       'filenames': ['US.zip', ],
#       'urls':      ['http://download.geonames.org/export/dump/'+'{filename}']
#    },
#}
#
#CITIES_POSTAL_CODES = ['US',]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

if 'EMAIL_HOST' in os.environ:
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = os.environ.get('EMAIL_PORT')
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
else:
    EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
    EMAIL_PORT = '587'
    DEFAULT_MAIL_FROM = ''
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 30
DEFAULT_MAIL_FROM = ''

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
if DEBUG:
    AWS_STORAGE_BUCKET_NAME = ''
else:
    AWS_STORAGE_BUCKET_NAME = ''

#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

TAGGABLE_COUNT = 25
