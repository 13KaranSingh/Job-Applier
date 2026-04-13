from datetime import datetime

from pydantic import BaseModel, Field


class JobSchema(BaseModel):
    id: str | None = None
    source_id: str
    external_job_id: str | None = None
    canonical_job_key: str
    company_name: str
    company_slug: str | None = None
    company_type: str = "other"
    title_raw: str
    title_normalized: str
    role_family: str
    experience_level: str
    location_raw: str | None = None
    location_normalized: str | None = None
    remote_policy: str = "unknown"
    posted_at_source: datetime | None = None
    first_seen_at: datetime | None = None
    apply_url: str
    detail_url: str
    description_text: str
    compensation_text: str | None = None
    base_salary_min_usd: float | None = None
    base_salary_max_usd: float | None = None
    auto_apply_supported: bool = False
    parser_confidence: float = 0.0
    automation_confidence: float = 0.0
    status: str = "new"


class JobScoreSchema(BaseModel):
    job_id: str
    total_score: float = 0
    recency_score: float = 0
    title_fit_score: float = 0
    seniority_fit_score: float = 0
    company_priority_score: float = 0
    prestige_score: float = 0
    compensation_score: float = 0
    location_fit_score: float = 0
    skills_fit_score: float = 0
    role_family_fit_score: float = 0
    source_quality_score: float = 0
    automation_readiness_score: float = 0
    friction_penalty: float = 0
    exclusion_penalty: float = 0
    recommended_resume_variant: str = "resume_swe_general.pdf"
    recommended_action: str = "QUEUE_FOR_REVIEW"
    explanations: list[str] = Field(default_factory=list)
    swe_score: float = 0
    quant_score: float = 0
    interview_probability: float = 0

