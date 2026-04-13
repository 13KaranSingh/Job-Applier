from celery import shared_task

from packages.db.bootstrap import create_all_tables
from packages.db.fixtures import load_sample_jobs
from packages.db.session import SessionLocal
from packages.source_seeding.seed_loader import build_default_sources
from packages.db.bootstrap import seed_default_sources


@shared_task(name="apps.worker.tasks.polling.poll_sources")
def poll_sources() -> dict[str, int]:
    create_all_tables()
    with SessionLocal() as session:
        seeded = seed_default_sources(session)
        discovered = load_sample_jobs(session)
    return {"seeded_sources": seeded, "discovered_jobs": discovered}
