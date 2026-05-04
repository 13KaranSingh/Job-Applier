from celery import shared_task

from packages.db.bootstrap import create_all_tables
from packages.db.session import SessionLocal
from packages.profile.local_setup import seed_local_profile


@shared_task(name="apps.worker.tasks.profile.seed_profile")
def seed_profile(path: str = "config/local/profile.json") -> dict[str, int]:
    create_all_tables()
    with SessionLocal() as session:
        return seed_local_profile(session, path)

