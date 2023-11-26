import os
import socket
from pathlib import Path
from .enums import  ModeEnum
from django.utils.translation import gettext_lazy as _
from environs import Env

# home/project/src/
BASE_DIR = Path(__file__).resolve().parent.parent


# Set Up environments variables
MODE = os.getenv('MODE', ModeEnum.DEV.value)

if MODE not in [ModeEnum._member_map_.get(mode).value for mode in ModeEnum._member_names_]:
    raise Exception("Model environment variable must be valid")

ENV_FILE = '.env.' + MODE

ENV_PATH = BASE_DIR.parent.joinpath("env").joinpath(ENV_FILE)

ENV = Env()

ENV.read_env(path=ENV_PATH)


# Application variables
SECRET_KEY = ENV('SECRET_KEY')

DEBUG = ENV('DEBUG')

ALLOWED_HOSTS = []

ROOT_URLCONF = 'settings.urls'

WSGI_APPLICATION = 'settings.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'


# Set up debug toolbar for docker
if DEBUG:
    hostname, p, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


# Applications definition
ROOT_APPS = [
    'apps.core',
    'apps.users',
    'apps.profiles',
    'apps.posts',
    ]

THIRD_PARTY_APPS = [
    'debug_toolbar',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    "phonenumber_field",
    ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *ROOT_APPS,
    *THIRD_PARTY_APPS,
]


# Niddlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]


# Templates
TEMPLATES_DIR = BASE_DIR.joinpath('templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]


# Static files
STATIC_URL = "static/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static/static"
]

MEDIA_ROOT = BASE_DIR.as_posix() + "/static/media/"
MEDIA_URL = MEDIA_ROOT


# Internalization
LOCALE_PATHS = [
    BASE_DIR.joinpath('locale'),
]

LANGUAGE_CODE = 'en'
LANGUAGE_COOKIE_NAME = 'en'

LANGUAGES = (
    ("en", _("English")),
    ("ru", _("Russian")),
)

USE_I18N = True


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ENV('POSTGRES_NAME'),
        'USER': ENV('POSTGRES_USER'),
        'PASSWORD': ENV('POSTGRES_PASSWORD'),
        'HOST': ENV('POSTGRES_HOST'),
        'PORT': ENV('POSTGRES_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Django-allauth
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
        ],
    },
}


# Time zone
TIME_ZONE = 'UTC'

USE_TZ = True
