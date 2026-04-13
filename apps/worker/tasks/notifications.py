from celery import shared_task


@shared_task(name="apps.worker.tasks.notifications.send_daily_digest")
def send_daily_digest() -> str:
    return "queued"

