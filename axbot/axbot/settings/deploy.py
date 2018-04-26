from .base import *

DEBUG = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'memcached:11211',
    }
}

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/var/www/static/'
STATIC_URL = '/static/'
