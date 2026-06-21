import json
import re
from html import unescape
from typing import Any

import httpx

from packages.adapters.base import BaseSourceAdapter
from packages.adapters.parsing.compensation import parse_compensation
from packages.adapters.parsing.normalization import (
    canonical_job_key,
    classify_experience_level,
    classify_role_family,
    normalize_company,
    normalize_location,
    normalize_title,
)
from packages.schemas.job import JobSchema

GOOGLE_JOB_PATTERN = re.compile(
    r'\["(?P<id>\d+)","(?P<title>[^"]+)","(?P<url>https://www\.google\.com/about/careers/applications/signin\?jobId[^"]+)"'
    r'.*?,"(?P<company>Google|YouTube)","en-US",\[\["(?P<location>[^"]+)"'
    r'.*?\],\[null,"(?P<description>.*?)"\]',
    re.DOTALL,
)


class GoogleAdapter(BaseSourceAdapter):
    source_name = "Google Careers"
    source_slug = "google"
    prefer_direct = True

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}

    async def discover_jobs(self) -> list[dict[str, Any]]:
        career_url = self.config.get("career_url") or "https://www.google.com/about/careers/applications/jobs/results/"
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(str(career_url))
            response.raise_for_status()
        return self.extract_jobs_from_html(response.text)

    def extract_jobs_from_html(self, html: str) -> list[dict[str, Any]]:
        jobs: list[dict[str, Any]] = []
        seen: set[str] = set()
        for match in GOOGLE_JOB_PATTERN.finditer(html):
            raw = match.groupdict()
            job_id = raw["id"]
            if job_id in seen:
                continue
            seen.add(job_id)
            jobs.append(
                {
                    "id": job_id,
                    "title": self._decode(raw["title"]),
                    "apply_url": self._decode(raw["url"]),
                    "company_name": self._decode(raw["company"]),
                    "location": self._decode(raw["location"]),
                    "description": self._decode(raw["description"]),
                }
            )
        return jobs

    def normalize_job(self, raw_job: dict[str, Any]) -> JobSchema:
        company = normalize_company(raw_job.get("company_name", "Google"))
        title_raw = raw_job.get("title", "")
        title = normalize_title(title_raw)
        location_raw = raw_job.get("location", "Unknown")
        location = normalize_location(location_raw)
        description = raw_job.get("description", "")
        compensation = parse_compensation(description)
        apply_url = raw_job.get("apply_url", "")
        external_id = str(raw_job.get("id", apply_url))
        return JobSchema(
            source_id=self.source_slug,
            external_job_id=external_id,
            canonical_job_key=canonical_job_key(company, title, location, external_id),
            company_name=company,
            company_slug=self.source_slug,
            title_raw=title_raw,
            title_normalized=title,
            role_family=classify_role_family(title, description),
            experience_level=classify_experience_level(title, description),
            location_raw=location_raw,
            location_normalized=location,
            apply_url=apply_url,
            detail_url=apply_url,
            description_text=description,
            compensation_text=description if compensation.compensation_confidence > 0 else None,
            base_salary_min_usd=compensation.base_salary_min_usd,
            base_salary_max_usd=compensation.base_salary_max_usd,
            auto_apply_supported=False,
            parser_confidence=0.94,
            automation_confidence=0.0,
            status="active",
        )

    async def get_job_detail(self, job_ref: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            response = await client.get(job_ref)
            response.raise_for_status()
        return {"job_ref": job_ref, "html": response.text}

    def supports_auto_apply(self) -> bool:
        return False

    async def apply(self, job: JobSchema, profile: dict[str, Any], resume_variant: str) -> dict[str, Any]:
        return {"status": "manual_review_required", "job_id": job.id, "resume_variant": resume_variant}

    async def healthcheck(self) -> dict[str, Any]:
        if not self.config.get("career_url"):
            return {"status": "not_configured"}
        try:
            jobs = await self.discover_jobs()
        except httpx.HTTPError as exc:
            return {"status": "degraded", "error": str(exc)}
        return {"status": "ok" if jobs else "empty"}

    def extract_metadata(self, raw_job: dict[str, Any]) -> dict[str, Any]:
        return {"parser_strategy": "google_inline_data"}

    def _decode(self, value: str) -> str:
        return unescape(json.loads(f'"{value}"'))
