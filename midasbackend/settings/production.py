# settings/production.py
from .base import *
from decouple import config, Csv
import dj_database_url

# Security
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')

# Allowed hosts
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# CORS
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())

# Database
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# Redirect all non-HTTPS requests to HTTPS (use in production)
SECURE_SSL_REDIRECT = True

# Set this to the header your proxy server sends when using HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True