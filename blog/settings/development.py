from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(" ")

DJANGO_APPS += []

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "rest_framework_simplejwt.token_blacklist",
]

LOCAL_APPS = ["apps.common", "apps.users", "apps.posts"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": env("POSTGRES_ENGINE"),
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("PG_HOST"),
        "PORT": env("PG_PORT"),
    }
}

# Allauth settings
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

LOGIN_URL = "http://localhost:8080/api/v1/login"
ACCOUNT_ADAPTER = "apps.users.adapter.CustomDefaultAccountAdapter"
ACTIVATE_EMAIL_URL = "http://localhost:8080"

#  Email Backend Config
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_USE_TLS = True
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "info@blog.com"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Email from blog - "


# logging

import logging
import logging.config

from django.utils.log import DEFAULT_LOGGING

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

LOG_LEVEL = "DEBUG"
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            # formatters defines what our log statements will look like.
            # %(asctime). This adds a timestamp to each message sent through the file handler.
            # %(name) – this is the package name that emits the log message
            # %(levelname) – the log level of the message (ERROR, WARNING, INFO, etc.)
            # %(message) – this is the actual log message
            # The -12s and the -8s control spacing between the different format specifications.
            "console": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            },
            "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "formatter": "file",
                "filename": "blog-debug.log",
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            "": {"level": "DEBUG", "handlers": ["console", "file"], "propagate": False},
            "apps": {
                "level": "DEBUG",
                "handlers": ["console"],
                # required to avoid double logging with root logger
                "propagate": False,
            },
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }
)
