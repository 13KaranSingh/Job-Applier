from celery import shared_task


@shared_task(name="apps.worker.tasks.cleanup.cleanup_old_artifacts")
def cleanup_old_artifacts() -> str:
    return "queued"

