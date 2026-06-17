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
    existing_sources = {source.slug: source for source in session.scalars(select(Source)).all()}
    for source_payload in build_default_sources():
        existing = existing_sources.get(source_payload["slug"])
        if existing is None:
            session.add(Source(**source_payload))
            created += 1
            continue
        config = dict(existing.config_json or {})
        for key, value in source_payload["config_json"].items():
            config.setdefault(key, value)
        existing.config_json = config
        session.add(existing)
    session.commit()
    return created
