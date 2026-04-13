from celery import shared_task


@shared_task(name="apps.worker.tasks.applications.run_auto_apply")
def run_auto_apply() -> str:
    return "queued"

