from celery import shared_task

from sqlalchemy import select

from packages.db.bootstrap import create_all_tables
from packages.db.models.job import Job, JobScore
from packages.db.models.profile import CandidateProfile
from packages.db.session import SessionLocal
from packages.ranking.scorer import CompanyMetadata, score_job
from packages.schemas.job import JobSchema
from packages.schemas.profile import CandidateProfileSchema
from packages.source_seeding.seed_loader import load_default_companies


@shared_task(name="apps.worker.tasks.ranking.rank_jobs")
def rank_jobs() -> str:
    create_all_tables()
    company_map = {item["company_name"]: item for item in load_default_companies()}
    with SessionLocal() as session:
        stored_profile = session.scalars(select(CandidateProfile).limit(1)).first()
        profile = CandidateProfileSchema(
            **stored_profile.profile_json
        ) if stored_profile else CandidateProfileSchema(
            full_name="Karan Singh",
            phone="unknown",
            current_city="Unknown",
            current_state="Unknown",
            github_url="",
            portfolio_url="",
            school_name="",
            degree="",
            major="",
            graduation_month="",
        )
        jobs = session.scalars(select(Job).where(Job.status.in_(["new", "active"]))).all()
        ranked = 0
        for job in jobs:
            metadata = company_map.get(job.company_name, {})
            score = score_job(
                JobSchema(
                    id=str(job.id),
                    source_id=str(job.source_id),
                    external_job_id=job.external_job_id,
                    canonical_job_key=job.canonical_job_key,
                    company_name=job.company_name,
                    company_slug=job.company_slug,
                    title_raw=job.title_raw,
                    title_normalized=job.title_normalized,
                    role_family=job.role_family,
                    experience_level=job.experience_level,
                    location_raw=job.location_raw,
                    location_normalized=job.location_normalized,
                    remote_policy=job.remote_policy,
                    posted_at_source=job.posted_at_source,
                    first_seen_at=job.first_seen_at,
                    apply_url=job.apply_url,
                    detail_url=job.detail_url,
                    description_text=job.description_text,
                    compensation_text=job.compensation_text,
                    base_salary_min_usd=float(job.base_salary_min_usd) if job.base_salary_min_usd is not None else None,
                    base_salary_max_usd=float(job.base_salary_max_usd) if job.base_salary_max_usd is not None else None,
                    auto_apply_supported=job.auto_apply_supported,
                    parser_confidence=job.parser_confidence,
                    automation_confidence=job.automation_confidence,
                    status=job.status,
                ),
                profile,
                CompanyMetadata(
                    target_priority=metadata.get("target_priority", 0),
                    prestige_tier=metadata.get("prestige_tier", 1),
                    compensation_tier=metadata.get("compensation_tier", 1),
                    role_bias=metadata.get("role_bias", "both"),
                    blacklisted=metadata.get("blacklisted", False),
                ),
            )
            record = session.scalars(select(JobScore).where(JobScore.job_id == job.id)).first()
            if record is None:
                record = JobScore(
                    job_id=job.id,
                    total_score=score.total_score,
                    recommended_resume_variant=score.recommended_resume_variant,
                    recommended_action=score.recommended_action,
                )
            record.total_score = score.total_score
            record.recency_score = score.recency_score
            record.title_fit_score = score.title_fit_score
            record.seniority_fit_score = score.seniority_fit_score
            record.company_priority_score = score.company_priority_score
            record.prestige_score = score.prestige_score
            record.compensation_score = score.compensation_score
            record.location_fit_score = score.location_fit_score
            record.skills_fit_score = score.skills_fit_score
            record.role_family_fit_score = score.role_family_fit_score
            record.source_quality_score = score.source_quality_score
            record.automation_readiness_score = score.automation_readiness_score
            record.friction_penalty = score.friction_penalty
            record.exclusion_penalty = score.exclusion_penalty
            record.quant_score = score.quant_score
            record.swe_score = score.swe_score
            record.interview_probability = score.interview_probability
            record.recommended_resume_variant = score.recommended_resume_variant
            record.recommended_action = score.recommended_action
            record.reasons_json = {"explanations": score.explanations}
            session.add(record)
            ranked += 1
        session.commit()
    return {"ranked_jobs": ranked}


@shared_task(name="apps.worker.tasks.ranking.decide_actions")
def decide_actions() -> str:
    with SessionLocal() as session:
        scores = session.scalars(select(JobScore)).all()
        counts = {"AUTO_APPLY_NOW": 0, "QUEUE_FOR_REVIEW": 0, "ALERT_ONLY": 0, "IGNORE": 0}
        for score in scores:
            counts[score.recommended_action] = counts.get(score.recommended_action, 0) + 1
    return counts
