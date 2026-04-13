from celery import shared_task


@shared_task(name="apps.worker.tasks.sheets_sync.sync_google_sheets")
def sync_google_sheets() -> str:
    return "queued"

