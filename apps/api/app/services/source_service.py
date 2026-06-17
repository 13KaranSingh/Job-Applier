from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.db.models.source import Source, SourceHealth
from packages.db.bootstrap import seed_default_sources


class SourceService:
    def list_sources(self, session: Session) -> list[Source]:
        return list(session.scalars(select(Source).order_by(Source.priority_weight.desc(), Source.name)).all())

    def list_sources_with_health(self, session: Session) -> list[tuple[Source, SourceHealth | None]]:
        return list(
            session.execute(
                select(Source, SourceHealth)
                .outerjoin(SourceHealth, SourceHealth.source_id == Source.id)
                .order_by(Source.priority_weight.desc(), Source.name)
            ).all()
        )

    def create_source(self, session: Session, payload: dict) -> Source:
        source = Source(
            name=payload["name"],
            slug=payload["slug"],
            source_type=payload.get("source_type", "company"),
            enabled=payload.get("enabled", True),
            polling_interval_seconds=int(payload.get("polling_interval_seconds", 600)),
            priority_weight=int(payload.get("priority_weight", 5)),
            supports_auto_apply=payload.get("supports_auto_apply", False),
            requires_login=payload.get("requires_login", False),
            config_json=payload.get("config_json", {}),
        )
        session.add(source)
        session.commit()
        session.refresh(source)
        return source

    def set_enabled(self, session: Session, source_id: str, enabled: bool) -> Source | None:
        source = session.get(Source, source_id)
        if source is None:
            return None
        source.enabled = enabled
        session.add(source)
        session.commit()
        session.refresh(source)
        return source

    def update_config(self, session: Session, source_id: str, payload: dict) -> Source | None:
        source = session.get(Source, source_id)
        if source is None:
            return None
        config = dict(source.config_json or {})
        for key in ["board_token", "company_slug", "company_name", "career_url", "ats_type"]:
            if key in payload:
                value = payload[key]
                if value in (None, ""):
                    config.pop(key, None)
                else:
                    config[key] = value
        source.config_json = config
        if "polling_interval_seconds" in payload:
            source.polling_interval_seconds = int(payload["polling_interval_seconds"])
        if "priority_weight" in payload:
            source.priority_weight = int(payload["priority_weight"])
        session.add(source)
        session.commit()
        session.refresh(source)
        return source

    def seed_defaults(self, session: Session) -> int:
        return seed_default_sources(session)
