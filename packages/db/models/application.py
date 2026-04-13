from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from packages.db.base import Base
from packages.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Application(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "applications"

    job_id: Mapped[str] = mapped_column(String(64), ForeignKey("jobs.id"), nullable=False, index=True)
    application_mode: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    resume_variant: Mapped[str] = mapped_column(String(255), nullable=False)
    started_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    submitted_at: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    confirmation_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    confirmation_text: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    failure_code: Mapped[str | None] = mapped_column(String(128))
    failure_stage: Mapped[str | None] = mapped_column(String(128))


class ApplicationEvent(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "application_events"

    application_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("applications.id"), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(String(128), nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

