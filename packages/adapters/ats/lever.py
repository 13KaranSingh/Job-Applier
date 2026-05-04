from typing import Any

import httpx

from packages.adapters.ats.greenhouse import GreenhouseAdapter
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


class LeverAdapter(GreenhouseAdapter):
    source_name = "Lever"
    source_slug = "lever"

    async def discover_jobs(self) -> list[dict[str, Any]]:
        company_slug = self.config.get("company_slug") or self.config.get("board_token")
        if not company_slug:
            return []
        url = f"https://api.lever.co/v0/postings/{company_slug}"
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            response = await client.get(url, params={"mode": "json"})
            response.raise_for_status()
            payload = response.json()
        if not isinstance(payload, list):
            return []
        company_name = self.config.get("company_name", company_slug)
        for job in payload:
            job["company_name"] = company_name
        return payload

    def normalize_job(self, raw_job: dict[str, Any]) -> JobSchema:
        company = normalize_company(raw_job.get("company_name") or self.config.get("company_name", "unknown"))
        title = normalize_title(raw_job.get("text", ""))
        categories = raw_job.get("categories") or {}
        location_raw = categories.get("location") or "Unknown"
        location = normalize_location(location_raw)
        description = " ".join(
            str(section.get("text", "")) for section in raw_job.get("lists", []) if isinstance(section, dict)
        )
        if not description:
            description = raw_job.get("descriptionPlain", "") or raw_job.get("description", "")
        compensation = parse_compensation(description)
        hosted_url = raw_job.get("hostedUrl", "")
        return JobSchema(
            source_id=self.source_slug,
            external_job_id=str(raw_job.get("id", "")),
            canonical_job_key=canonical_job_key(company, title, location, raw_job.get("id")),
            company_name=company,
            title_raw=raw_job.get("text", ""),
            title_normalized=title,
            role_family=classify_role_family(title, description),
            experience_level=classify_experience_level(title, description),
            location_raw=location_raw,
            location_normalized=location,
            apply_url=hosted_url,
            detail_url=hosted_url,
            description_text=description,
            compensation_text=description if compensation.compensation_confidence > 0 else None,
            base_salary_min_usd=compensation.base_salary_min_usd,
            base_salary_max_usd=compensation.base_salary_max_usd,
            auto_apply_supported=False,
            parser_confidence=0.88,
            automation_confidence=0.0,
            status="active",
        )

    async def healthcheck(self) -> dict[str, Any]:
        company_slug = self.config.get("company_slug") or self.config.get("board_token")
        if not company_slug:
            return {"status": "not_configured"}
        try:
            await self.discover_jobs()
        except httpx.HTTPError as exc:
            return {"status": "degraded", "error": str(exc)}
        return {"status": "ok"}

    def extract_metadata(self, raw_job: dict[str, Any]) -> dict[str, Any]:
        return {"ats_type": "lever"}
