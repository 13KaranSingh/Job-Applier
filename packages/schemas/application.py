from datetime import datetime

from pydantic import BaseModel


class ApplicationSchema(BaseModel):
    id: str | None = None
    job_id: str
    application_mode: str
    status: str
    resume_variant: str
    started_at: datetime | None = None
    submitted_at: datetime | None = None
    confirmation_detected: bool = False
    confirmation_text: str | None = None
    notes: str | None = None
    failure_code: str | None = None
    failure_stage: str | None = None

