import asyncio

from celery import shared_task
from sqlalchemy import select

from apps.api.app.config import get_settings
from packages.adapters.registry import ADAPTER_REGISTRY
from packages.adapters.generic import GenericCareersAdapter
from packages.db.bootstrap import create_all_tables
from packages.db.bootstrap import seed_default_sources
from packages.db.fixtures import load_sample_jobs, purge_sample_jobs
from packages.db.models.job import Job
from packages.db.models.source import Source, SourceHealth
from packages.db.session import SessionLocal
from packages.core.utils.datetime import utcnow


def _select_adapter_class(source: Source):
    config = source.config_json or {}
    adapter_class = ADAPTER_REGISTRY.get(source.slug)
    if adapter_class is not None and getattr(adapter_class, "prefer_direct", False):
        return adapter_class
    if config.get("career_url") and not (config.get("board_token") or config.get("company_slug")):
        return GenericCareersAdapter
    if adapter_class is None and config.get("career_url"):
        return GenericCareersAdapter
    return adapter_class


async def _discover_source(source: Source) -> list:
    adapter_class = _select_adapter_class(source)
    if adapter_class is None:
        return []
    config = {**source.config_json, "source_slug": source.slug}
    adapter = adapter_class(config)
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


def _reconcile_source_jobs(session, source: Source, normalized_jobs: list) -> int:
    active_jobs = session.scalars(
        select(Job).where(Job.source_id == source.id, Job.status == "active")
    ).all()
    seen_keys = {job.canonical_job_key for job in normalized_jobs}
    closed = 0
    for existing in active_jobs:
        if existing.canonical_job_key in seen_keys:
            continue
        existing.status = "closed"
        session.add(existing)
        closed += 1
    return closed


@shared_task(name="apps.worker.tasks.polling.poll_sources")
def poll_sources() -> dict[str, int]:
    create_all_tables()
    settings = get_settings()
    with SessionLocal() as session:
        seeded = seed_default_sources(session)
        fixture_jobs = load_sample_jobs(session) if settings.enable_fixture_jobs else 0
        purged_fixture_jobs = purge_sample_jobs(session) if not settings.enable_fixture_jobs else 0
        adapter_jobs = 0
        sources = session.scalars(select(Source).where(Source.enabled.is_(True))).all()
        for source in sources:
            try:
                adapter_class = _select_adapter_class(source)
                if adapter_class is None:
                    health = session.scalars(select(SourceHealth).where(SourceHealth.source_id == source.id)).first()
                    if health is None:
                        health = SourceHealth(source_id=source.id, status="not_supported")
                    health.status = "not_supported"
                    health.last_failure_at = utcnow().isoformat()
                    health.recent_error_summary = "No adapter registered for this source."
                    session.add(health)
                    continue
                adapter = adapter_class({**source.config_json, "source_slug": source.slug})
                health_result = asyncio.run(adapter.healthcheck())
                status = health_result.get("status", "unknown")
                if status != "ok":
                    health = session.scalars(select(SourceHealth).where(SourceHealth.source_id == source.id)).first()
                    if health is None:
                        health = SourceHealth(source_id=source.id, status=status)
                    health.status = status
                    if status not in {"paused", "not_configured"}:
                        health.last_failure_at = utcnow().isoformat()
                    health.recent_error_summary = health_result.get("error")
                    session.add(health)
                    continue
                normalized_jobs = asyncio.run(_discover_source(source))
                _reconcile_source_jobs(session, source, normalized_jobs)
                adapter_jobs += _upsert_jobs(session, source, normalized_jobs)
                health = session.scalars(select(SourceHealth).where(SourceHealth.source_id == source.id)).first()
                if health is None:
                    health = SourceHealth(source_id=source.id, status="ok")
                health.status = "ok"
                health.last_success_at = utcnow().isoformat()
                health.recent_error_summary = None
                session.add(health)
            except Exception as exc:
                health = session.scalars(select(SourceHealth).where(SourceHealth.source_id == source.id)).first()
                if health is None:
                    health = SourceHealth(source_id=source.id, status="degraded")
                health.status = "degraded"
                health.last_failure_at = utcnow().isoformat()
                health.recent_error_summary = str(exc)
                session.add(health)
        session.commit()
    return {
        "seeded_sources": seeded,
        "fixture_jobs": fixture_jobs,
        "purged_fixture_jobs": purged_fixture_jobs,
        "adapter_jobs": adapter_jobs,
    }
