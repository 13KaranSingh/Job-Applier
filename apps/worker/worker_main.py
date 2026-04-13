from celery import Celery

from apps.api.app.config import get_settings

settings = get_settings()

celery_app = Celery("job_bot", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_default_queue = "job-bot"
celery_app.autodiscover_tasks(["apps.worker.tasks"])

