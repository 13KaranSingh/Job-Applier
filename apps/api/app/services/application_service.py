from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from packages.db.models.application import Application
from packages.db.models.job import Job


class ApplicationService:
    def list_applications(self, session: Session, limit: int = 100) -> list[tuple[Application, Job]]:
        return list(
            session.execute(
                select(Application, Job)
                .join(Job, Job.id == Application.job_id)
                .order_by(desc(Application.created_at))
                .limit(limit)
            ).all()
        )

    def get_application(self, session: Session, application_id: str) -> Application | None:
        return session.get(Application, application_id)

    def retry_application(self, session: Session, application_id: str) -> Application | None:
        application = session.get(Application, application_id)
        if application is None:
            return None
        application.status = "PENDING"
        session.add(application)
        session.commit()
        session.refresh(application)
        return application
