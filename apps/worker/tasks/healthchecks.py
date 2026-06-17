import asyncio

from celery import shared_task
from sqlalchemy import select

from packages.adapters.generic import GenericCareersAdapter
from packages.adapters.registry import ADAPTER_REGISTRY
from packages.core.utils.datetime import utcnow
from packages.db.models.source import Source, SourceHealth
from packages.db.session import SessionLocal


async def _check_source(source: Source) -> dict[str, str]:
    adapter_class = ADAPTER_REGISTRY.get(source.slug)
    if adapter_class is None and source.config_json.get("career_url"):
        adapter_class = GenericCareersAdapter
    if adapter_class is None:
        return {"status": "not_supported", "error": "No adapter registered"}
    config = {**source.config_json, "source_slug": source.slug}
    adapter = adapter_class(config)
    result = await adapter.healthcheck()
    if not isinstance(result, dict):
        return {"status": "degraded", "error": "Invalid healthcheck payload"}
    return {str(key): str(value) for key, value in result.items()}


@shared_task(name="apps.worker.tasks.healthchecks.healthcheck_sources")
def healthcheck_sources() -> dict[str, int]:
    with SessionLocal() as session:
        sources = session.scalars(select(Source)).all()
        updated = 0
        for source in sources:
            record = session.scalars(select(SourceHealth).where(SourceHealth.source_id == source.id)).first()
            if record is None:
                record = SourceHealth(source_id=source.id, status="ok")
            if not source.enabled:
                record.status = "paused"
            else:
                try:
                    result = asyncio.run(_check_source(source))
                    record.status = result.get("status", "unknown")
                    record.recent_error_summary = result.get("error")
                    if record.status == "ok":
                        record.last_success_at = utcnow().isoformat()
                    elif record.status not in {"paused", "not_configured"}:
                        record.last_failure_at = utcnow().isoformat()
                except Exception as exc:
                    record.status = "degraded"
                    record.recent_error_summary = str(exc)
                    record.last_failure_at = utcnow().isoformat()
            session.add(record)
            updated += 1
        session.commit()
    return {"sources_checked": updated}
