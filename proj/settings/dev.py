from .defaults import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dev-db.sqlite3'),
    }
}

# Celery settings
CELERY_BROKER_URL = 'redis://redis:6379/8'
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://127.0.0.1:8080']
