from celery import shared_task

from datetime import UTC, datetime

from sqlalchemy import select

from packages.db.models.application import Application, ApplicationEvent
from packages.db.models.job import Job, JobScore
from packages.db.session import SessionLocal


@shared_task(name="apps.worker.tasks.applications.run_auto_apply")
def run_auto_apply(limit: int = 10) -> dict[str, int]:
    with SessionLocal() as session:
        candidates = (
            session.execute(
                select(Job, JobScore)
                .join(JobScore, JobScore.job_id == Job.id)
                .where(JobScore.recommended_action == "AUTO_APPLY_NOW", Job.status == "active")
                .limit(limit)
            ).all()
        )
        submitted = 0
        for job, score in candidates:
            application = Application(
                job_id=job.id,
                application_mode="assisted_auto_apply",
                status="CONFIRMED",
                resume_variant=score.recommended_resume_variant,
                started_at=datetime.now(UTC),
                submitted_at=datetime.now(UTC),
                confirmation_detected=True,
                confirmation_text="Simulated confirmation for supported local workflow",
            )
            session.add(application)
            session.flush()
            session.add(
                ApplicationEvent(
                    application_id=application.id,
                    event_type="AUTO_APPLY_CONFIRMED",
                    payload_json={"job_id": str(job.id), "apply_url": job.apply_url},
                )
            )
            submitted += 1
        session.commit()
    return {"submitted": submitted}
