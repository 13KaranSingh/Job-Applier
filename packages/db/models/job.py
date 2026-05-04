import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from packages.db.base import Base
from packages.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Job(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "jobs"

    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False, index=True)
    external_job_id: Mapped[str | None] = mapped_column(String(255))
    canonical_job_key: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    company_slug: Mapped[str | None] = mapped_column(String(255))
    company_domain: Mapped[str | None] = mapped_column(String(255))
    title_raw: Mapped[str] = mapped_column(String(255), nullable=False)
    title_normalized: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    team_or_org: Mapped[str | None] = mapped_column(String(255))
    location_raw: Mapped[str | None] = mapped_column(String(255))
    location_normalized: Mapped[str | None] = mapped_column(String(255), index=True)
    remote_policy: Mapped[str] = mapped_column(String(50), default="unknown", nullable=False)
    employment_type: Mapped[str | None] = mapped_column(String(50))
    target_track: Mapped[str] = mapped_column(String(50), default="both", nullable=False)
    role_family: Mapped[str] = mapped_column(String(50), default="other", nullable=False)
    experience_level: Mapped[str] = mapped_column(String(50), default="unknown", nullable=False)
    posted_at_source: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    first_seen_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    last_seen_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    apply_url: Mapped[str] = mapped_column(Text, nullable=False)
    detail_url: Mapped[str] = mapped_column(Text, nullable=False)
    description_text: Mapped[str] = mapped_column(Text, nullable=False)
    compensation_text: Mapped[str | None] = mapped_column(Text)
    compensation_min: Mapped[float | None] = mapped_column(Numeric(12, 2))
    compensation_max: Mapped[float | None] = mapped_column(Numeric(12, 2))
    base_salary_min_usd: Mapped[float | None] = mapped_column(Numeric(12, 2))
    base_salary_max_usd: Mapped[float | None] = mapped_column(Numeric(12, 2))
    auto_apply_supported: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    parser_confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    automation_confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="new", nullable=False)
    raw_payload_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)


class JobAlias(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "job_aliases"

    canonical_job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False, index=True)
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)
    external_job_id: Mapped[str | None] = mapped_column(String(255))
    alias_url: Mapped[str | None] = mapped_column(Text)


class JobScore(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "job_scores"

    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False, index=True)
    total_score: Mapped[float] = mapped_column(Float, nullable=False)
    recency_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    title_fit_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    seniority_fit_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    company_priority_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    prestige_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    compensation_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    location_fit_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    skills_fit_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    role_family_fit_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    source_quality_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    automation_readiness_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    friction_penalty: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    exclusion_penalty: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    quant_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    swe_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    interview_probability: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    recommended_resume_variant: Mapped[str] = mapped_column(String(255), nullable=False)
    recommended_action: Mapped[str] = mapped_column(String(50), nullable=False)
    reasons_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
