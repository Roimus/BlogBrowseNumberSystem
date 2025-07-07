import eventlet
eventlet.monkey_patch()

import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogBrowseNumberSystem.settings')
app = Celery('BlogBrowseNumberSystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()