# -*- coding:UTF-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
# from kombu import serialization
#
# serialization.registry._decoders.pop("application/x-python-serialize")
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baoma.settings')

app = Celery('baoma')

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
