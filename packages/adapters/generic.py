from typing import Any

import httpx

from packages.adapters.base import BaseSourceAdapter
from packages.adapters.parsing.compensation import parse_compensation
from packages.adapters.parsing.html import extract_job_links, extract_text
from packages.adapters.parsing.jsonld import extract_jsonld_blocks
from packages.adapters.parsing.normalization import (
    canonical_job_key,
    classify_experience_level,
    classify_role_family,
    normalize_company,
    normalize_location,
    normalize_title,
)
from packages.schemas.job import JobSchema


class GenericCareersAdapter(BaseSourceAdapter):
    source_name = "Generic Careers Page"
    source_slug = "generic-careers"

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}

    async def discover_jobs(self) -> list[dict[str, Any]]:
        career_url = self.config.get("career_url")
        if not career_url:
            return []
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            response = await client.get(str(career_url))
            response.raise_for_status()
        html = response.text
        postings: list[dict[str, Any]] = []
        for block in extract_jsonld_blocks(html):
            candidates = block if isinstance(block, list) else [block]
            for candidate in candidates:
                if not isinstance(candidate, dict):
                    continue
                if candidate.get("@type") == "JobPosting":
                    postings.append({**candidate, "source_html_text": extract_text(html)})
        if postings:
            return postings
        for link in extract_job_links(html, str(career_url)):
            postings.append(
                {
                    "@type": "JobPosting",
                    "title": link["title"],
                    "url": link["url"],
                    "description": "",
                    "company_name": self.config.get("company_name", "Unknown"),
                    "parser_strategy": "html_links",
                    "source_html_text": "",
                }
            )
        return postings

    def normalize_job(self, raw_job: dict[str, Any]) -> JobSchema:
        company_payload = raw_job.get("hiringOrganization") or {}
        company = normalize_company(
            self.config.get("company_name")
            or company_payload.get("name")
            or raw_job.get("company_name")
            or "Unknown"
        )
        title_raw = raw_job.get("title", "")
        title = normalize_title(title_raw)
        location_raw = self._location(raw_job)
        location = normalize_location(location_raw)
        description = extract_text(raw_job.get("description", "")) or raw_job.get("source_html_text", "")
        compensation = parse_compensation(description)
        detail_url = raw_job.get("url") or self.config.get("career_url") or ""
        external_id = raw_job.get("identifier") or detail_url or title_raw
        return JobSchema(
            source_id=self.config.get("source_slug", self.source_slug),
            external_job_id=str(external_id),
            canonical_job_key=canonical_job_key(company, title, location, external_id),
            company_name=company,
            company_slug=self.config.get("company_slug"),
            title_raw=title_raw,
            title_normalized=title,
            role_family=classify_role_family(title, description),
            experience_level=classify_experience_level(title, description),
            location_raw=location_raw,
            location_normalized=location,
            posted_at_source=None,
            apply_url=str(detail_url),
            detail_url=str(detail_url),
            description_text=description or title,
            compensation_text=description if compensation.compensation_confidence > 0 else None,
            base_salary_min_usd=compensation.base_salary_min_usd,
            base_salary_max_usd=compensation.base_salary_max_usd,
            auto_apply_supported=False,
            parser_confidence=0.72 if raw_job.get("parser_strategy") != "html_links" else 0.58,
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
            await self.discover_jobs()
        except httpx.HTTPError as exc:
            return {"status": "degraded", "error": str(exc)}
        return {"status": "ok"}

    def extract_metadata(self, raw_job: dict[str, Any]) -> dict[str, Any]:
        return {"parser_strategy": raw_job.get("parser_strategy", "jsonld")}

    def _location(self, raw_job: dict[str, Any]) -> str:
        location = raw_job.get("jobLocation")
        if isinstance(location, list):
            location = location[0] if location else None
        if isinstance(location, dict):
            address = location.get("address") or {}
            if isinstance(address, dict):
                parts = [
                    address.get("addressLocality"),
                    address.get("addressRegion"),
                    address.get("addressCountry"),
                ]
                return ", ".join(str(part) for part in parts if part)
        return str(self.config.get("default_location") or "Unknown")
