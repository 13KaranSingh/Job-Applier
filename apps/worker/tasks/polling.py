from celery import shared_task


@shared_task(name="apps.worker.tasks.polling.poll_sources")
def poll_sources() -> str:
    return "queued"

