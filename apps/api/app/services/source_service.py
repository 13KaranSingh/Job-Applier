from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.db.models.source import Source
from packages.db.bootstrap import seed_default_sources


class SourceService:
    def list_sources(self, session: Session) -> list[Source]:
        return list(session.scalars(select(Source).order_by(Source.priority_weight.desc(), Source.name)).all())

    def set_enabled(self, session: Session, source_id: str, enabled: bool) -> Source | None:
        source = session.get(Source, source_id)
        if source is None:
            return None
        source.enabled = enabled
        session.add(source)
        session.commit()
        session.refresh(source)
        return source

    def seed_defaults(self, session: Session) -> int:
        return seed_default_sources(session)
