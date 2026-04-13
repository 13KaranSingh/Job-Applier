from celery import shared_task

from sqlalchemy import select

from packages.db.models.source import Source, SourceHealth
from packages.db.session import SessionLocal


@shared_task(name="apps.worker.tasks.healthchecks.healthcheck_sources")
def healthcheck_sources() -> dict[str, int]:
    with SessionLocal() as session:
        sources = session.scalars(select(Source)).all()
        updated = 0
        for source in sources:
            record = session.scalars(select(SourceHealth).where(SourceHealth.source_id == source.id)).first()
            if record is None:
                record = SourceHealth(source_id=source.id, status="ok")
            record.status = "ok" if source.enabled else "paused"
            session.add(record)
            updated += 1
        session.commit()
    return {"sources_checked": updated}
