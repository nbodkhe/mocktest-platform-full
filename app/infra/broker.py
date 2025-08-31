from celery import Celery
from app.core.config import settings
celery_app = Celery("mocktest")
celery_app.conf.broker_url = settings.BROKER_URL
celery_app.conf.result_backend = settings.RESULT_BACKEND
