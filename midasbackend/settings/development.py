# settings/development.py
from .base import *
from decouple import config, Csv

DEBUG = True

SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Redirect all non-HTTPS requests to HTTPS (use in production)
SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = False