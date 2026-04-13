from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from packages.db.models.application import Application


class ApplicationService:
    def list_applications(self, session: Session, limit: int = 100) -> list[Application]:
        return list(session.scalars(select(Application).order_by(desc(Application.created_at)).limit(limit)).all())

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
