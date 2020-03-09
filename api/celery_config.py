from __future__ import absolute_import, unicode_literals
import os
import celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = celery.Celery('api', broker=settings.CELERY_BROKER_URL)
# set up a once Q so that we can lock tasks to a single run at any one time.
app.conf.ONCE = settings.CELERY_ONCE_CONFIG
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
