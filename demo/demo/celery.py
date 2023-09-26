import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
app = Celery("demo")
# app.config_from_object("django.conf.settings")
# # app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# app.autodiscover_tasks()
# Load the Celery configuration from Django settings
app.config_from_object(settings, namespace='CELERY')
# app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
