from pydantic import BaseModel


class SourceSchema(BaseModel):
    id: str | None = None
    name: str
    slug: str
    source_type: str
    enabled: bool = True
    polling_interval_seconds: int = 600
    priority_weight: int = 1
    supports_auto_apply: bool = False
    requires_login: bool = False
    config_json: dict = {}

