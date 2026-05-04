import asyncio

from celery import shared_task
from sqlalchemy import select

from packages.adapters.registry import ADAPTER_REGISTRY
from packages.db.bootstrap import create_all_tables
from packages.db.bootstrap import seed_default_sources
from packages.db.fixtures import load_sample_jobs
from packages.db.models.job import Job
from packages.db.models.source import Source, SourceHealth
from packages.db.session import SessionLocal
from packages.core.utils.datetime import utcnow


async def _discover_source(source: Source) -> list:
    adapter_class = ADAPTER_REGISTRY.get(source.slug)
    if adapter_class is None:
        return []
    adapter = adapter_class(source.config_json)
    raw_jobs = await adapter.discover_jobs()
    return [adapter.normalize_job(raw_job) for raw_job in raw_jobs]


def _upsert_jobs(session, source: Source, normalized_jobs: list) -> int:
    created = 0
    for normalized in normalized_jobs:
        seen_at = normalized.first_seen_at or utcnow()
        existing = session.scalars(
            select(Job).where(Job.canonical_job_key == normalized.canonical_job_key)
        ).first()
        if existing is not None:
            existing.last_seen_at = seen_at
            existing.status = "active"
            session.add(existing)
            continue
        session.add(
            Job(
                source_id=source.id,
                external_job_id=normalized.external_job_id,
                canonical_job_key=normalized.canonical_job_key,
                company_name=normalized.company_name,
                company_slug=normalized.company_slug or source.slug,
                title_raw=normalized.title_raw,
                title_normalized=normalized.title_normalized,
                location_raw=normalized.location_raw,
                location_normalized=normalized.location_normalized,
                remote_policy=normalized.remote_policy,
                target_track=normalized.role_family,
                role_family=normalized.role_family,
                experience_level=normalized.experience_level,
                posted_at_source=normalized.posted_at_source,
                first_seen_at=seen_at,
                last_seen_at=seen_at,
                apply_url=normalized.apply_url,
                detail_url=normalized.detail_url,
                description_text=normalized.description_text,
                compensation_text=normalized.compensation_text,
                base_salary_min_usd=normalized.base_salary_min_usd,
                base_salary_max_usd=normalized.base_salary_max_usd,
                auto_apply_supported=normalized.auto_apply_supported,
                parser_confidence=normalized.parser_confidence,
                automation_confidence=normalized.automation_confidence,
                status="active",
                raw_payload_json=normalized.model_dump(mode="json"),
            )
        )
        created += 1
    return created


@shared_task(name="apps.worker.tasks.polling.poll_sources")
def poll_sources() -> dict[str, int]:
    create_all_tables()
    with SessionLocal() as session:
        seeded = seed_default_sources(session)
        discovered = load_sample_jobs(session)
        adapter_jobs = 0
        sources = session.scalars(select(Source).where(Source.enabled.is_(True))).all()
        for source in sources:
            try:
                normalized_jobs = asyncio.run(_discover_source(source))
                adapter_jobs += _upsert_jobs(session, source, normalized_jobs)
                health = session.scalars(select(SourceHealth).where(SourceHealth.source_id == source.id)).first()
                if health is None:
                    health = SourceHealth(source_id=source.id, status="ok")
                health.status = "ok"
                session.add(health)
            except Exception as exc:
                health = session.scalars(select(SourceHealth).where(SourceHealth.source_id == source.id)).first()
                if health is None:
                    health = SourceHealth(source_id=source.id, status="degraded")
                health.status = "degraded"
                health.recent_error_summary = str(exc)
                session.add(health)
        session.commit()
    return {"seeded_sources": seeded, "fixture_jobs": discovered, "adapter_jobs": adapter_jobs}
