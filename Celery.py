import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Campus_Connect.settings")

app = Celery("Campus_Connect")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()