import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.adapters.parsing.compensation import parse_compensation
from packages.adapters.parsing.normalization import (
    canonical_job_key,
    classify_experience_level,
    classify_role_family,
    normalize_location,
    normalize_title,
)
from packages.db.models.job import Job
from packages.db.models.source import Source


def load_sample_jobs(session: Session, fixture_path: str = "data/fixtures/sample_jobs.json") -> int:
    path = Path(fixture_path)
    if not path.exists():
        return 0
    payload = json.loads(path.read_text())
    sources = {source.slug: source for source in session.scalars(select(Source)).all()}
    created = 0
    for item in payload:
        source = sources.get(item["source_slug"])
        if source is None:
            continue
        title_normalized = normalize_title(item["title"])
        location_normalized = normalize_location(item["location"])
        job_key = canonical_job_key(
            item["company_name"], title_normalized, location_normalized, item["external_job_id"]
        )
        existing = session.scalars(select(Job).where(Job.canonical_job_key == job_key)).first()
        if existing is not None:
            continue
        compensation = parse_compensation(item.get("compensation_text"))
        posted_at = datetime.now(UTC) - timedelta(hours=item.get("posted_hours_ago", 24))
        session.add(
            Job(
                source_id=source.id,
                external_job_id=item["external_job_id"],
                canonical_job_key=job_key,
                company_name=item["company_name"],
                company_slug=item["source_slug"],
                title_raw=item["title"],
                title_normalized=title_normalized,
                location_raw=item["location"],
                location_normalized=location_normalized,
                remote_policy=item.get("remote_policy", "unknown"),
                target_track=classify_role_family(title_normalized, item["description_text"]),
                role_family=classify_role_family(title_normalized, item["description_text"]),
                experience_level=classify_experience_level(title_normalized, item["description_text"]),
                posted_at_source=posted_at,
                first_seen_at=datetime.now(UTC),
                last_seen_at=datetime.now(UTC),
                apply_url=item["apply_url"],
                detail_url=item["detail_url"],
                description_text=item["description_text"],
                compensation_text=item.get("compensation_text"),
                compensation_min=compensation.base_salary_min_usd,
                compensation_max=compensation.base_salary_max_usd,
                base_salary_min_usd=compensation.base_salary_min_usd,
                base_salary_max_usd=compensation.base_salary_max_usd,
                auto_apply_supported=item.get("auto_apply_supported", False),
                parser_confidence=0.95,
                automation_confidence=0.60,
                status="active",
                raw_payload_json=item,
            )
        )
        created += 1
    session.commit()
    return created

