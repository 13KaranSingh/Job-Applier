from celery import shared_task

from sqlalchemy import select

from packages.db.models.job import Job, JobScore
from packages.db.session import SessionLocal
from packages.notifications.digest_builder import build_daily_digest
from packages.notifications.service import NotificationService
from packages.notifications.yahoo_mailer import top_job_email


@shared_task(name="apps.worker.tasks.notifications.send_daily_digest")
def send_daily_digest() -> dict[str, int]:
    with SessionLocal() as session:
        service = NotificationService()
        summary = {
            "jobs_discovered": session.query(Job).count(),
            "applications_submitted": session.query(JobScore).filter(JobScore.recommended_action == "AUTO_APPLY_NOW").count(),
            "applications_failed": 0,
        }
        service.enqueue(
            session,
            "daily_digest",
            "[Job Bot] Daily Digest",
            {"text_body": build_daily_digest(summary)},
        )
        sent = service.send_pending(session)
    return {"sent": sent}


@shared_task(name="apps.worker.tasks.notifications.send_top_job_alerts")
def send_top_job_alerts(limit: int = 5) -> dict[str, int]:
    with SessionLocal() as session:
        service = NotificationService()
        rows = (
            session.execute(
                select(Job, JobScore)
                .join(JobScore, JobScore.job_id == Job.id)
                .where(
                    JobScore.total_score >= 70,
                    Job.status == "active",
                    JobScore.recommended_action != "IGNORE",
                )
                .limit(limit)
            ).all()
        )
        queued = 0
        for job, score in rows:
            subject, text, html = top_job_email(
                job.company_name,
                job.title_normalized,
                job.location_normalized or "Unknown",
                score.total_score,
                job.apply_url,
            )
            service.enqueue(
                session,
                "new_top_job",
                subject,
                {"text_body": text, "html_body": html, "job_id": str(job.id)},
            )
            queued += 1
        sent = service.send_pending(session)
    return {"queued": queued, "sent": sent}
