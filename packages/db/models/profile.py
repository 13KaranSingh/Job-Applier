from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from packages.db.base import Base
from packages.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class CandidateProfile(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "candidate_profile"

    profile_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    updated_at: Mapped[str | None] = mapped_column(String(64))


class AnswerLibrary(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "answer_library"

    answer_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    prompt_patterns_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    requires_human_review: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    updated_at: Mapped[str | None] = mapped_column(String(64))


class ResumeAsset(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "resume_assets"

    variant_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    updated_at: Mapped[str | None] = mapped_column(String(64))

