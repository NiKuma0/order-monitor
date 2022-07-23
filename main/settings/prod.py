import os

from main.settings.base import *  # noqa

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': (
            os.getenv('REDIS_URL') or
            f'redis://{os.getenv("REDIS_USER")}:{os.getenv("REDIS_PASSWORD")}'
            f'@{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}/1'
        ),
        'TIMEOUT': 60*60*24*29,  # One month
    }
}

# Celery

CELERY_RESULT_BACKEND = CELERY_BROKER_URL = (
    os.getenv('REDIS_URL') or
    f'redis://{os.getenv("REDIS_USER")}:{os.getenv("REDIS_PASSWORD")}'
    f'@{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}/0'
)
