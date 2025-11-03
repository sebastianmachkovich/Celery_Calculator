from celery import Celery

app = Celery('calculator')
app.config_from_object('celery_config')

from app import tasks
