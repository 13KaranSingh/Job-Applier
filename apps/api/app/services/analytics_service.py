from sqlalchemy import func, select
from sqlalchemy.orm import Session

from packages.db.models.application import Application
from packages.db.models.job import Job, JobScore
from packages.db.models.source import Source, SourceHealth


class AnalyticsService:
    def get_summary(self, session: Session) -> dict:
        jobs_discovered = session.scalar(select(func.count()).select_from(Job)) or 0
        applications_submitted = session.scalar(select(func.count()).select_from(Application)) or 0
        jobs_above_70 = session.scalar(
            select(func.count()).select_from(JobScore).where(JobScore.total_score >= 70)
        ) or 0
        active_sources = session.scalar(
            select(func.count()).select_from(Source).where(Source.enabled.is_(True))
        ) or 0
        degraded_sources = session.scalar(
            select(func.count()).select_from(SourceHealth).where(SourceHealth.status != "ok")
        ) or 0
        return {
            "jobs_discovered": jobs_discovered,
            "applications_submitted": applications_submitted,
            "jobs_above_70": jobs_above_70,
            "active_sources": active_sources,
            "degraded_sources": degraded_sources,
        }
