from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from packages.core.enums import SortMode
from packages.core.utils.datetime import utcnow
from packages.db.models.application import Application, ApplicationEvent
from packages.db.models.job import Job, JobScore
from packages.ranking.decision import classify_decision
from packages.ranking.queue import sort_top_jobs
from packages.ranking.scorer import CompanyMetadata, score_job
from packages.schemas.job import JobSchema
from packages.schemas.profile import CandidateProfileSchema
from packages.source_seeding.seed_loader import load_default_companies


class JobService:
    def list_jobs(self, session: Session, limit: int = 100) -> list[Job]:
        return list(session.scalars(select(Job).order_by(desc(Job.first_seen_at)).limit(limit)).all())

    def get_job(self, session: Session, job_id: str) -> Job | None:
        return session.get(Job, job_id)

    def list_top_jobs(
        self,
        session: Session,
        limit: int = 50,
        sort_mode: SortMode = SortMode.BEST_OVERALL,
        track: str | None = None,
        remote_only: bool = False,
        auto_apply_only: bool = False,
    ) -> list[dict]:
        rows = session.execute(
            select(Job, JobScore)
            .join(JobScore, JobScore.job_id == Job.id)
            .where(Job.status == "active", JobScore.total_score >= 70)
            .order_by(desc(JobScore.total_score), desc(Job.posted_at_source))
            .limit(limit)
        ).all()
        items = [
            {
                "id": str(job.id),
                "company_name": job.company_name,
                "title_normalized": job.title_normalized,
                "location_normalized": job.location_normalized,
                "remote_policy": job.remote_policy,
                "role_family": job.role_family,
                "status": job.status,
                "apply_url": job.apply_url,
                "source_name": job.company_name,
                "posted_at_source": job.posted_at_source,
                "first_seen_at": job.first_seen_at,
                "total_score": score.total_score,
                "compensation_score": score.compensation_score,
                "prestige_score": score.prestige_score,
                "quant_score": score.quant_score,
                "swe_score": score.swe_score,
                "automation_readiness_score": score.automation_readiness_score,
                "recency_score": score.recency_score,
                "company_priority_score": score.company_priority_score,
                "location_fit_score": score.location_fit_score,
                "recommended_action": score.recommended_action,
                "auto_apply_supported": job.auto_apply_supported,
            }
            for job, score in rows
        ]
        if track in {"swe", "quant", "both"}:
            items = [item for item in items if item["role_family"] == track or (track != "both" and item["role_family"] == "both")]
        if remote_only:
            items = [item for item in items if item["remote_policy"] == "remote"]
        if auto_apply_only:
            items = [item for item in items if item["auto_apply_supported"]]
        return sort_top_jobs(items, sort_mode=sort_mode)

    def rerank_job(self, session: Session, job_id: str) -> dict[str, str] | None:
        job = session.get(Job, job_id)
        if job is None:
            return None
        profile = CandidateProfileSchema(
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
        company_map = {item["company_name"]: item for item in load_default_companies()}
        company = company_map.get(job.company_name, {})
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
                target_priority=company.get("target_priority", 0),
                prestige_tier=company.get("prestige_tier", 1),
                compensation_tier=company.get("compensation_tier", 1),
                role_bias=company.get("role_bias", "both"),
                blacklisted=company.get("blacklisted", False),
            ),
        )
        existing = session.scalars(select(JobScore).where(JobScore.job_id == job.id)).first()
        if existing is None:
            existing = JobScore(job_id=job.id, total_score=0, recommended_resume_variant="resume_swe_general.pdf", recommended_action="IGNORE")
        existing.total_score = score.total_score
        existing.recency_score = score.recency_score
        existing.title_fit_score = score.title_fit_score
        existing.seniority_fit_score = score.seniority_fit_score
        existing.company_priority_score = score.company_priority_score
        existing.prestige_score = score.prestige_score
        existing.compensation_score = score.compensation_score
        existing.location_fit_score = score.location_fit_score
        existing.skills_fit_score = score.skills_fit_score
        existing.role_family_fit_score = score.role_family_fit_score
        existing.source_quality_score = score.source_quality_score
        existing.automation_readiness_score = score.automation_readiness_score
        existing.friction_penalty = score.friction_penalty
        existing.exclusion_penalty = score.exclusion_penalty
        existing.recommended_resume_variant = score.recommended_resume_variant
        existing.recommended_action = score.recommended_action
        existing.reasons_json = {"explanations": score.explanations}
        existing.quant_score = score.quant_score
        existing.swe_score = score.swe_score
        existing.interview_probability = score.interview_probability
        session.add(existing)
        session.commit()
        return {"job_id": job_id, "decision": classify_decision(score).value}

    def apply_job(self, session: Session, job_id: str) -> dict[str, str] | None:
        job = session.get(Job, job_id)
        if job is None:
            return None
        existing = session.scalars(select(Application).where(Application.job_id == job.id)).first()
        if existing is not None:
            return {"job_id": job_id, "application_id": str(existing.id), "status": existing.status}
        score = session.scalars(select(JobScore).where(JobScore.job_id == job.id)).first()
        resume_variant = (
            score.recommended_resume_variant
            if score is not None and score.recommended_resume_variant
            else "resume_swe_general.pdf" if job.role_family != "quant" else "resume_quant_swe.pdf"
        )
        application = Application(
            job_id=job.id,
            application_mode="manual_handoff",
            status="MANUAL_REVIEW_REQUIRED",
            resume_variant=resume_variant,
            started_at=utcnow(),
            notes="Manual handoff created from dashboard/API apply action.",
        )
        session.add(application)
        session.flush()
        session.add(
            ApplicationEvent(
                application_id=application.id,
                event_type="MANUAL_REVIEW_REQUIRED",
                payload_json={"job_id": job_id, "apply_url": job.apply_url},
            )
        )
        session.commit()
        session.refresh(application)
        return {"job_id": job_id, "application_id": str(application.id), "status": application.status}
