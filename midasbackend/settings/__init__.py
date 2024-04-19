# settings/__init__.py
from decouple import config
from .base import *

ENV = config('DJANGO_ENV')


if ENV == 'production':
    from .production import *
else:
    from .development import *
