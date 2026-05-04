"""initial schema"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260413_0001"
down_revision = None
branch_labels = None
depends_on = None


def timestamps() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
    ]


def uuid_pk() -> sa.Column:
    return sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False)


def upgrade() -> None:
    op.create_table(
        "sources",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("polling_interval_seconds", sa.Integer(), nullable=False),
        sa.Column("priority_weight", sa.Integer(), nullable=False),
        sa.Column("supports_auto_apply", sa.Boolean(), nullable=False),
        sa.Column("requires_login", sa.Boolean(), nullable=False),
        sa.Column("config_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        uuid_pk(),
        *timestamps(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_sources_slug"), "sources", ["slug"], unique=True)

    op.create_table(
        "jobs",
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("external_job_id", sa.String(length=255), nullable=True),
        sa.Column("canonical_job_key", sa.String(length=512), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("company_slug", sa.String(length=255), nullable=True),
        sa.Column("company_domain", sa.String(length=255), nullable=True),
        sa.Column("title_raw", sa.String(length=255), nullable=False),
        sa.Column("title_normalized", sa.String(length=255), nullable=False),
        sa.Column("team_or_org", sa.String(length=255), nullable=True),
        sa.Column("location_raw", sa.String(length=255), nullable=True),
        sa.Column("location_normalized", sa.String(length=255), nullable=True),
        sa.Column("remote_policy", sa.String(length=50), nullable=False),
        sa.Column("employment_type", sa.String(length=50), nullable=True),
        sa.Column("target_track", sa.String(length=50), nullable=False),
        sa.Column("role_family", sa.String(length=50), nullable=False),
        sa.Column("experience_level", sa.String(length=50), nullable=False),
        sa.Column("posted_at_source", sa.DateTime(timezone=True), nullable=True),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("apply_url", sa.Text(), nullable=False),
        sa.Column("detail_url", sa.Text(), nullable=False),
        sa.Column("description_text", sa.Text(), nullable=False),
        sa.Column("compensation_text", sa.Text(), nullable=True),
        sa.Column("compensation_min", sa.Numeric(12, 2), nullable=True),
        sa.Column("compensation_max", sa.Numeric(12, 2), nullable=True),
        sa.Column("base_salary_min_usd", sa.Numeric(12, 2), nullable=True),
        sa.Column("base_salary_max_usd", sa.Numeric(12, 2), nullable=True),
        sa.Column("auto_apply_supported", sa.Boolean(), nullable=False),
        sa.Column("parser_confidence", sa.Float(), nullable=False),
        sa.Column("automation_confidence", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("raw_payload_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        uuid_pk(),
        *timestamps(),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("canonical_job_key"),
    )
    op.create_index(op.f("ix_jobs_company_name"), "jobs", ["company_name"], unique=False)
    op.create_index(op.f("ix_jobs_location_normalized"), "jobs", ["location_normalized"], unique=False)
    op.create_index(op.f("ix_jobs_source_id"), "jobs", ["source_id"], unique=False)
    op.create_index(op.f("ix_jobs_title_normalized"), "jobs", ["title_normalized"], unique=False)

    op.create_table(
        "applications",
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("application_mode", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("resume_variant", sa.String(length=255), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("confirmation_detected", sa.Boolean(), nullable=False),
        sa.Column("confirmation_text", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("failure_code", sa.String(length=128), nullable=True),
        sa.Column("failure_stage", sa.String(length=128), nullable=True),
        uuid_pk(),
        *timestamps(),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_applications_job_id"), "applications", ["job_id"], unique=False)

    op.create_table(
        "application_events",
        sa.Column("application_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("payload_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        uuid_pk(),
        sa.ForeignKeyConstraint(["application_id"], ["applications.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_application_events_application_id"), "application_events", ["application_id"], unique=False)

    op.create_table(
        "job_aliases",
        sa.Column("canonical_job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("external_job_id", sa.String(length=255), nullable=True),
        sa.Column("alias_url", sa.Text(), nullable=True),
        uuid_pk(),
        sa.ForeignKeyConstraint(["canonical_job_id"], ["jobs.id"]),
        sa.ForeignKeyConstraint(["source_id"], ["sources.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_job_aliases_canonical_job_id"), "job_aliases", ["canonical_job_id"], unique=False)

    op.create_table(
        "job_scores",
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("total_score", sa.Float(), nullable=False),
        sa.Column("recency_score", sa.Float(), nullable=False),
        sa.Column("title_fit_score", sa.Float(), nullable=False),
        sa.Column("seniority_fit_score", sa.Float(), nullable=False),
        sa.Column("company_priority_score", sa.Float(), nullable=False),
        sa.Column("prestige_score", sa.Float(), nullable=False),
        sa.Column("compensation_score", sa.Float(), nullable=False),
        sa.Column("location_fit_score", sa.Float(), nullable=False),
        sa.Column("skills_fit_score", sa.Float(), nullable=False),
        sa.Column("role_family_fit_score", sa.Float(), nullable=False),
        sa.Column("source_quality_score", sa.Float(), nullable=False),
        sa.Column("automation_readiness_score", sa.Float(), nullable=False),
        sa.Column("friction_penalty", sa.Float(), nullable=False),
        sa.Column("exclusion_penalty", sa.Float(), nullable=False),
        sa.Column("quant_score", sa.Float(), nullable=False),
        sa.Column("swe_score", sa.Float(), nullable=False),
        sa.Column("interview_probability", sa.Float(), nullable=False),
        sa.Column("recommended_resume_variant", sa.String(length=255), nullable=False),
        sa.Column("recommended_action", sa.String(length=50), nullable=False),
        sa.Column("reasons_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        uuid_pk(),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_job_scores_job_id"), "job_scores", ["job_id"], unique=False)

    op.create_table(
        "candidate_profile",
        sa.Column("profile_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("updated_at", sa.String(length=64), nullable=True),
        uuid_pk(),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "answer_library",
        sa.Column("answer_key", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=255), nullable=False),
        sa.Column("prompt_patterns_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("answer_text", sa.Text(), nullable=False),
        sa.Column("requires_human_review", sa.Boolean(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("updated_at", sa.String(length=64), nullable=True),
        uuid_pk(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("answer_key"),
    )

    op.create_table(
        "resume_assets",
        sa.Column("variant_name", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.Text(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("updated_at", sa.String(length=64), nullable=True),
        uuid_pk(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("variant_name"),
    )

    op.create_table(
        "notifications",
        sa.Column("notification_type", sa.String(length=128), nullable=False),
        sa.Column("target_email", sa.String(length=255), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("payload_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        uuid_pk(),
        *timestamps(),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "source_health",
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("last_success_at", sa.String(length=64), nullable=True),
        sa.Column("last_failure_at", sa.String(length=64), nullable=True),
        sa.Column("recent_error_summary", sa.Text(), nullable=True),
        uuid_pk(),
        *timestamps(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_source_health_source_id"), "source_health", ["source_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_source_health_source_id"), table_name="source_health")
    op.drop_table("source_health")
    op.drop_table("notifications")
    op.drop_table("resume_assets")
    op.drop_table("answer_library")
    op.drop_table("candidate_profile")
    op.drop_index(op.f("ix_job_scores_job_id"), table_name="job_scores")
    op.drop_table("job_scores")
    op.drop_index(op.f("ix_job_aliases_canonical_job_id"), table_name="job_aliases")
    op.drop_table("job_aliases")
    op.drop_index(op.f("ix_application_events_application_id"), table_name="application_events")
    op.drop_table("application_events")
    op.drop_index(op.f("ix_applications_job_id"), table_name="applications")
    op.drop_table("applications")
    op.drop_index(op.f("ix_jobs_title_normalized"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_source_id"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_location_normalized"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_company_name"), table_name="jobs")
    op.drop_table("jobs")
    op.drop_index(op.f("ix_sources_slug"), table_name="sources")
    op.drop_table("sources")
