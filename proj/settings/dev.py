from .defaults import *

DEBUG = True

ALLOWED_HOSTS.extend(["127.0.0.1", "0.0.0.0"])

# Celery settings
CELERY_BROKER_URL = 'redis://redis:6379/8'
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://127.0.0.1:8080']
