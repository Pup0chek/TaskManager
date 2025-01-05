import os
import time

from celery import Celery
from src.mail import send_email

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://taskmanager-redis_task-1:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://taskmanager-redis_task-1:6379")


@celery.task(name="create_task")
def create_task(mail, topic, text):
    time.sleep(10)
    send_email(mail, topic, text)
    return True