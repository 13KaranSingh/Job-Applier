from typing import Any

import httpx
from bs4 import BeautifulSoup

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

JANE_STREET_JOBS_URL = "https://www.janestreet.com/jobs/main.json"
JANE_STREET_OPEN_IDS_URL = "https://www.janestreet.com/static/position-directories.json"
JANE_STREET_POSITION_URL = "https://www.janestreet.com/join-jane-street/position/{job_id}/"

CITY_LABELS = {
    "AMS": "Amsterdam, Netherlands",
    "ATX": "Austin, TX",
    "CHI": "Chicago, IL",
    "HKG": "Hong Kong",
    "LDN": "London, UK",
    "MUM": "Mumbai, India",
    "NYC": "New York, NY",
    "PHL": "Philadelphia, PA",
    "SF": "San Francisco, CA",
    "SGP": "Singapore",
    "SHA": "Shanghai, China",
}


class JaneStreetAdapter(BaseSourceAdapter):
    source_name = "Jane Street"
    source_slug = "jane-street"
    prefer_direct = True

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}

    async def discover_jobs(self) -> list[dict[str, Any]]:
        jobs_url = self.config.get("jobs_url") or JANE_STREET_JOBS_URL
        open_ids_url = self.config.get("open_ids_url") or JANE_STREET_OPEN_IDS_URL
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            jobs_response = await client.get(str(jobs_url))
            jobs_response.raise_for_status()
            open_ids_response = await client.get(str(open_ids_url))
            open_ids_response.raise_for_status()

        jobs_payload = jobs_response.json()
        open_ids_payload = open_ids_response.json()
        if not isinstance(jobs_payload, list):
            return []
        open_ids = {str(item) for item in open_ids_payload} if isinstance(open_ids_payload, list) else set()
        if not open_ids:
            return [job for job in jobs_payload if isinstance(job, dict)]
        return [
            job
            for job in jobs_payload
            if isinstance(job, dict) and str(job.get("id", "")) in open_ids
        ]

    def normalize_job(self, raw_job: dict[str, Any]) -> JobSchema:
        company = normalize_company("Jane Street")
        title_raw = str(raw_job.get("position", ""))
        title = normalize_title(title_raw)
        location_raw = self._city_label(str(raw_job.get("city", "Unknown")))
        location = normalize_location(location_raw)
        description = self._description_text(raw_job)
        salary_text = self._salary_text(raw_job)
        compensation = parse_compensation(salary_text or description)
        min_salary = self._salary_value(raw_job.get("min_salary")) or compensation.base_salary_min_usd
        max_salary = self._salary_value(raw_job.get("max_salary")) or compensation.base_salary_max_usd
        external_id = str(raw_job.get("id", ""))
        detail_url = JANE_STREET_POSITION_URL.format(job_id=external_id)
        return JobSchema(
            source_id=self.source_slug,
            external_job_id=external_id,
            canonical_job_key=canonical_job_key(company, title, location, external_id),
            company_name=company,
            company_slug=self.source_slug,
            company_type="quant",
            title_raw=title_raw,
            title_normalized=title,
            role_family=classify_role_family(title, description),
            experience_level=classify_experience_level(title, description),
            location_raw=location_raw,
            location_normalized=location,
            apply_url=detail_url,
            detail_url=detail_url,
            description_text=description,
            compensation_text=salary_text,
            base_salary_min_usd=min_salary,
            base_salary_max_usd=max_salary,
            auto_apply_supported=False,
            parser_confidence=0.96,
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
        try:
            jobs = await self.discover_jobs()
        except httpx.HTTPError as exc:
            return {"status": "degraded", "error": str(exc)}
        return {"status": "ok" if jobs else "empty"}

    def extract_metadata(self, raw_job: dict[str, Any]) -> dict[str, Any]:
        return {
            "parser_strategy": "jane_street_json",
            "team": raw_job.get("team"),
            "category": raw_job.get("category"),
            "availability": raw_job.get("availability"),
            "duration": raw_job.get("duration"),
        }

    def _description_text(self, raw_job: dict[str, Any]) -> str:
        overview = str(raw_job.get("overview") or "")
        text = BeautifulSoup(overview, "lxml").get_text(" ", strip=True)
        metadata = [
            str(raw_job.get("category") or ""),
            str(raw_job.get("team") or ""),
            str(raw_job.get("availability") or ""),
            str(raw_job.get("duration") or ""),
        ]
        return " ".join([part for part in [*metadata, text] if part]).strip()

    def _salary_text(self, raw_job: dict[str, Any]) -> str | None:
        min_salary = raw_job.get("min_salary")
        max_salary = raw_job.get("max_salary")
        if min_salary and max_salary:
            return f"${min_salary} - ${max_salary}"
        if min_salary:
            return f"${min_salary}+"
        if max_salary:
            return f"Up to ${max_salary}"
        return None

    def _salary_value(self, value: Any) -> float | None:
        if value in (None, ""):
            return None
        try:
            return float(str(value).replace(",", ""))
        except ValueError:
            return None

    def _city_label(self, value: str) -> str:
        parts = [part.strip() for part in value.split("/") if part.strip()]
        if not parts:
            return "Unknown"
        return " / ".join(CITY_LABELS.get(part, part) for part in parts)
