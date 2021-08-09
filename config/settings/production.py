import os

from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["photographic.aer.dev"]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
    }
}


# Media
# https://docs.djangoproject.com/en/3.1/ref/settings/#media-root
# https://docs.djangoproject.com/en/3.1/ref/settings/#media-url

DEFAULT_FILE_STORAGE = "config.storages.MediaStorage"

MEDIA_URL = os.environ["MEDIA_STORAGE_URL"]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_STORAGE = "config.storages.StaticStorage"

STATICFILES_DIRS = [APPS_DIR / "static"]

STATIC_URL = os.environ["STATIC_STORAGE_URL"]
