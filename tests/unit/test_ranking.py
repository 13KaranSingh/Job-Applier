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
    assert score.total_score >= 70
    assert score.recommended_action in {"AUTO_APPLY_NOW", "QUEUE_FOR_REVIEW", "ALERT_ONLY"}
    assert "Strong title fit" in score.explanations


def test_elite_quant_role_uses_quant_score_in_balanced_mode() -> None:
    profile = CandidateProfileSchema(
        full_name="Karan Singh",
        phone="555-555-5555",
        current_city="Newark",
        current_state="DE",
        github_url="https://github.com/13KaranSingh",
        portfolio_url="https://karan.codes",
        school_name="University of Delaware",
        degree="BS",
        major="Computer Science",
        graduation_month="May",
        skill_inventory=["python", "c++", "statistics", "probability", "trading systems"],
    )
    job = JobSchema(
        source_id="jane-street",
        canonical_job_key="key",
        company_name="Jane Street",
        title_raw="Quantitative Researcher",
        title_normalized="quantitative researcher",
        role_family="quant",
        experience_level="entry",
        location_raw="New York, NY",
        location_normalized="New York, NY",
        remote_policy="onsite",
        apply_url="https://www.janestreet.com/join-jane-street/position/1/",
        detail_url="https://www.janestreet.com/join-jane-street/position/1/",
        description_text="Use Python C++ probability statistics market microstructure and research.",
        base_salary_max_usd=300000,
        parser_confidence=0.96,
        automation_confidence=0,
        status="active",
    )
    metadata = CompanyMetadata(target_priority=99, prestige_tier=5, compensation_tier=5, role_bias="quant")

    score = score_job(job, profile, metadata, operating_mode=OperatingMode.BALANCED)

    assert score.total_score >= 70
    assert score.recommended_action == "QUEUE_FOR_REVIEW"
    assert "High-prestige company" in score.explanations


def test_parser_confidence_alone_does_not_queue_low_score_job() -> None:
    profile = CandidateProfileSchema(
        full_name="Karan Singh",
        phone="555-555-5555",
        current_city="Newark",
        current_state="DE",
        github_url="https://github.com/13KaranSingh",
        portfolio_url="https://karan.codes",
        school_name="University of Delaware",
        degree="BS",
        major="Computer Science",
        graduation_month="May",
    )
    job = JobSchema(
        source_id="generic",
        canonical_job_key="key",
        company_name="Unknown Co",
        title_raw="Operations Analyst",
        title_normalized="operations analyst",
        role_family="other",
        experience_level="unknown",
        location_raw="Unknown",
        location_normalized="Unknown",
        apply_url="https://example.com/jobs/1",
        detail_url="https://example.com/jobs/1",
        description_text="Unrelated operations role.",
        parser_confidence=0.95,
        automation_confidence=0,
        status="active",
    )

    score = score_job(job, profile, CompanyMetadata(), operating_mode=OperatingMode.BALANCED)

    assert score.total_score < 55
    assert score.recommended_action == "IGNORE"
