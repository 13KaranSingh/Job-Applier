from celery import shared_task


@shared_task(name="apps.worker.tasks.healthchecks.healthcheck_sources")
def healthcheck_sources() -> str:
    return "queued"

