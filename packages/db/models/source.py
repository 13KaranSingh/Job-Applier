from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from packages.db.base import Base
from packages.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Source(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "sources"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    polling_interval_seconds: Mapped[int] = mapped_column(Integer, default=600, nullable=False)
    priority_weight: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    supports_auto_apply: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    requires_login: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    config_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)


class SourceHealth(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "source_health"

    source_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    last_success_at: Mapped[str | None] = mapped_column(String(64))
    last_failure_at: Mapped[str | None] = mapped_column(String(64))
    recent_error_summary: Mapped[str | None] = mapped_column(Text)

