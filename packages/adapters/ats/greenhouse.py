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


class GreenhouseAdapter(BaseSourceAdapter):
    source_name = "Greenhouse"
    source_slug = "greenhouse"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}

    async def discover_jobs(self) -> list[dict[str, Any]]:
        board_token = self.config.get("board_token")
        if not board_token:
            return []
        url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            response = await client.get(url, params={"content": "true"})
            response.raise_for_status()
            payload = response.json()
        jobs = payload.get("jobs", [])
        if not isinstance(jobs, list):
            return []
        company_name = self.config.get("company_name", board_token)
        for job in jobs:
            job["company_name"] = company_name
        return jobs

    def normalize_job(self, raw_job: dict[str, Any]) -> JobSchema:
        company = normalize_company(raw_job.get("company_name", "unknown"))
        title = normalize_title(raw_job.get("title", ""))
        location_payload = raw_job.get("location") or {}
        location_raw = location_payload.get("name") if isinstance(location_payload, dict) else str(location_payload)
        location = normalize_location(location_raw or "Unknown")
        description = raw_job.get("content", "")
        compensation = parse_compensation(description)
        return JobSchema(
            source_id=self.source_slug,
            external_job_id=str(raw_job.get("id", "")),
            canonical_job_key=canonical_job_key(company, title, location, raw_job.get("id")),
            company_name=company,
            title_raw=raw_job.get("title", ""),
            title_normalized=title,
            role_family=classify_role_family(title, description),
            experience_level=classify_experience_level(title, description),
            location_raw=location_raw,
            location_normalized=location,
            apply_url=raw_job.get("absolute_url", ""),
            detail_url=raw_job.get("absolute_url", ""),
            description_text=description,
            compensation_text=description if compensation.compensation_confidence > 0 else None,
            base_salary_min_usd=compensation.base_salary_min_usd,
            base_salary_max_usd=compensation.base_salary_max_usd,
            auto_apply_supported=False,
            parser_confidence=0.90,
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
        board_token = self.config.get("board_token")
        if not board_token:
            return {"status": "not_configured"}
        try:
            await self.discover_jobs()
        except httpx.HTTPError as exc:
            return {"status": "degraded", "error": str(exc)}
        return {"status": "ok"}

    def extract_metadata(self, raw_job: dict[str, Any]) -> dict[str, Any]:
        return {"ats_type": "greenhouse"}
