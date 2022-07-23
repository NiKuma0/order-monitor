from main.settings.base import *  # noqa


SECRET_KEY = 'django-insecure-rys47f=_fcqd1(ut2p#ys!_mrw&u*bbks#o#j6+w2nrnc7!ypb'

DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'TIMEOUT': 60*60*24*29,
    }
}

# Celery

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
