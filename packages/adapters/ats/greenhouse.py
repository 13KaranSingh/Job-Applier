from typing import Any

from packages.adapters.base import BaseSourceAdapter
from packages.adapters.parsing.normalization import canonical_job_key, normalize_company, normalize_title
from packages.schemas.job import JobSchema


class GreenhouseAdapter(BaseSourceAdapter):
    source_name = "Greenhouse"
    source_slug = "greenhouse"

    async def discover_jobs(self) -> list[dict[str, Any]]:
        return []

    def normalize_job(self, raw_job: dict[str, Any]) -> JobSchema:
        company = normalize_company(raw_job.get("company_name", "unknown"))
        title = normalize_title(raw_job.get("title", ""))
        location = raw_job.get("location", "Unknown")
        return JobSchema(
            source_id=self.source_slug,
            external_job_id=str(raw_job.get("id", "")),
            canonical_job_key=canonical_job_key(company, title, location, raw_job.get("id")),
            company_name=company,
            title_raw=raw_job.get("title", ""),
            title_normalized=title,
            role_family="other",
            experience_level="unknown",
            location_raw=location,
            location_normalized=location,
            apply_url=raw_job.get("absolute_url", ""),
            detail_url=raw_job.get("absolute_url", ""),
            description_text=raw_job.get("content", ""),
        )

    async def get_job_detail(self, job_ref: str) -> dict[str, Any]:
        return {"job_ref": job_ref}

    def supports_auto_apply(self) -> bool:
        return False

    async def apply(self, job: JobSchema, profile: dict[str, Any], resume_variant: str) -> dict[str, Any]:
        return {"status": "manual_review_required", "job_id": job.id, "resume_variant": resume_variant}

    async def healthcheck(self) -> dict[str, Any]:
        return {"status": "ok"}

    def extract_metadata(self, raw_job: dict[str, Any]) -> dict[str, Any]:
        return {"ats_type": "greenhouse"}

