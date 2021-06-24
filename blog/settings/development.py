from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(" ")

DJANGO_APPS += []

THIRD_PARTY_APPS = ["rest_framework"]

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
