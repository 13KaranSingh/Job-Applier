from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.db.base import Base
from packages.db.models.source import Source
from packages.db.session import engine
from packages.source_seeding.seed_loader import build_default_sources


def create_all_tables() -> None:
    Base.metadata.create_all(bind=engine)


def seed_default_sources(session: Session) -> int:
    created = 0
    existing = {
        slug for slug in session.scalars(select(Source.slug)).all()
    }
    for source_payload in build_default_sources():
        if source_payload["slug"] in existing:
            continue
        session.add(Source(**source_payload))
        created += 1
    session.commit()
    return created

