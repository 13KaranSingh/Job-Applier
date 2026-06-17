from pathlib import Path
from typing import Any
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from apps.api.app.config import get_settings
from packages.db.models.application import Application
from packages.db.models.job import Job, JobScore
from packages.tracker.csv_sync import write_csv


class TrackerService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.export_root = Path(self.settings.storage_root) / "exports"

    def sync_csv_exports(self, session: Session) -> dict[str, str]:
        applications_rows = self._application_rows(session)
        top_jobs_rows = self._top_jobs_rows(session)
        job_feed_rows = self._job_feed_rows(session)
        failures_rows = [row for row in applications_rows if row["status"].startswith("FAILED")]
        daily_stats_rows = self._daily_stats_rows(session)
        files = {
            "applications": self.export_root / "Applications.csv",
            "top_jobs": self.export_root / "TopJobs.csv",
            "job_feed": self.export_root / "JobFeed.csv",
            "failures": self.export_root / "Failures.csv",
            "daily_stats": self.export_root / "DailyStats.csv",
        }
        write_csv(files["applications"], applications_rows)
        write_csv(files["top_jobs"], top_jobs_rows)
        write_csv(files["job_feed"], job_feed_rows)
        write_csv(files["failures"], failures_rows)
        write_csv(files["daily_stats"], daily_stats_rows)
        return {name: str(path) for name, path in files.items()}

    def _application_rows(self, session: Session) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        results = session.execute(select(Application, Job).join(Job, Job.id == Application.job_id)).all()
        for application, job in results:
            rows.append(
                {
                    "internal_application_id": str(application.id),
                    "discovered_at": job.first_seen_at,
                    "posted_at_source": job.posted_at_source,
                    "applied_at": application.submitted_at,
                    "company": job.company_name,
                    "title": job.title_normalized,
                    "target_track": job.target_track,
                    "location": job.location_normalized,
                    "source_name": job.company_name,
                    "apply_url": job.apply_url,
                    "detail_url": job.detail_url,
                    "ats_type": job.company_slug,
                    "status": application.status,
                    "resume_variant": application.resume_variant,
                    "confirmation_detected": application.confirmation_detected,
                    "notes": application.notes,
                }
            )
        return rows

    def _top_jobs_rows(self, session: Session) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        results = session.execute(select(Job, JobScore).join(JobScore, JobScore.job_id == Job.id)).all()
        for job, score in results:
            if score.total_score < 70 or job.status != "active":
                continue
            rows.append(
                {
                    "internal_job_id": str(job.id),
                    "company": job.company_name,
                    "title": job.title_normalized,
                    "location": job.location_normalized,
                    "source_name": job.company_name,
                    "posted_at_source": job.posted_at_source,
                    "discovered_at": job.first_seen_at,
                    "total_score": score.total_score,
                    "top_match_reasons": ", ".join(score.reasons_json.get("explanations", [])),
                    "auto_apply_supported": job.auto_apply_supported,
                    "current_status": job.status,
                    "action_link": job.apply_url,
                }
            )
        return rows

    def _job_feed_rows(self, session: Session) -> list[dict[str, Any]]:
        jobs = session.scalars(select(Job).order_by(Job.first_seen_at.desc())).all()
        return [
            {
                "internal_job_id": str(job.id),
                "company": job.company_name,
                "title": job.title_normalized,
                "location": job.location_normalized,
                "posted_at_source": job.posted_at_source,
                "discovered_at": job.first_seen_at,
                "status": job.status,
                "apply_url": job.apply_url,
            }
            for job in jobs
        ]

    def _daily_stats_rows(self, session: Session) -> list[dict[str, Any]]:
        today = datetime.now(UTC).date().isoformat()
        jobs_discovered = session.scalar(select(func.count()).select_from(Job)) or 0
        jobs_scored = session.scalar(select(func.count()).select_from(JobScore)) or 0
        jobs_above_70 = session.scalar(select(func.count()).select_from(JobScore).where(JobScore.total_score >= 70)) or 0
        jobs_above_85 = session.scalar(select(func.count()).select_from(JobScore).where(JobScore.total_score >= 85)) or 0
        applications_submitted = (
            session.scalar(
                select(func.count()).select_from(Application).where(Application.status.in_(["SUBMITTED", "CONFIRMED"]))
            )
            or 0
        )
        applications_failed = (
            session.scalar(select(func.count()).select_from(Application).where(Application.status.like("FAILED%"))) or 0
        )
        review_queue_count = (
            session.scalar(select(func.count()).select_from(JobScore).where(JobScore.recommended_action == "QUEUE_FOR_REVIEW"))
            or 0
        )
        top_company_row = session.execute(
            select(Job.company_name, func.count(Job.id).label("count"))
            .group_by(Job.company_name)
            .order_by(func.count(Job.id).desc())
        ).first()
        top_company = top_company_row[0] if top_company_row else ""
        return [
            {
                "date": today,
                "jobs_discovered": jobs_discovered,
                "jobs_scored": jobs_scored,
                "jobs_above_70": jobs_above_70,
                "jobs_above_85": jobs_above_85,
                "applications_submitted": applications_submitted,
                "applications_failed": applications_failed,
                "review_queue_count": review_queue_count,
                "avg_time_to_discovery_minutes": "",
                "avg_time_to_apply_minutes": "",
                "top_source": top_company,
                "top_company": top_company,
            }
        ]
