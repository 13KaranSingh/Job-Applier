from datetime import UTC, datetime, timedelta

from packages.core.enums import OperatingMode
from packages.ranking.scorer import CompanyMetadata, score_job
from packages.schemas.job import JobSchema
from packages.schemas.profile import CandidateProfileSchema


def test_high_quality_recent_google_job_scores_for_review_or_better() -> None:
    profile = CandidateProfileSchema(
        full_name="Karan Singh",
        phone="555-555-5555",
        current_city="Jersey City",
        current_state="NJ",
        github_url="https://github.com/13KaranSingh",
        portfolio_url="https://karan.codes",
        school_name="Example University",
        degree="BS",
        major="Computer Science",
        graduation_month="May",
    )
    job = JobSchema(
        source_id="google",
        canonical_job_key="key",
        company_name="Google",
        title_raw="Software Engineer, Early Career",
        title_normalized="software engineer early career",
        role_family="swe",
        experience_level="new_grad",
        location_raw="New York City",
        location_normalized="New York City",
        remote_policy="hybrid",
        posted_at_source=datetime.now(UTC) - timedelta(hours=1),
        apply_url="https://careers.google.com/jobs/1",
        detail_url="https://careers.google.com/jobs/1",
        description_text="React TypeScript Python distributed systems early career",
        base_salary_max_usd=220000,
        auto_apply_supported=True,
        parser_confidence=0.92,
        automation_confidence=0.90,
        status="active",
    )
    metadata = CompanyMetadata(target_priority=98, prestige_tier=5, compensation_tier=5, role_bias="swe")
    score = score_job(job, profile, metadata, operating_mode=OperatingMode.BALANCED)
    assert score.total_score >= 55
    assert score.recommended_action in {"AUTO_APPLY_NOW", "QUEUE_FOR_REVIEW", "ALERT_ONLY"}
    assert "Strong title fit" in score.explanations

