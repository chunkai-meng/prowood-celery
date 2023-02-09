#!/bin/sh
# uwsgi -d /var/uwsgi/uwsgi_demoapp.log /home/proj/uwsgi.ini
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
python manage.py runserver --settings=proj.settings.dev
celery -A proj worker -l info
