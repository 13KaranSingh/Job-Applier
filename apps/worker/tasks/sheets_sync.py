from celery import shared_task

from packages.db.session import SessionLocal
from packages.tracker.service import TrackerService


@shared_task(name="apps.worker.tasks.sheets_sync.sync_google_sheets")
def sync_google_sheets() -> dict[str, str]:
    with SessionLocal() as session:
        return TrackerService().sync_csv_exports(session)
