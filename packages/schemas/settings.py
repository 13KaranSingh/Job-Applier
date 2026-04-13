from pydantic import BaseModel


class OperatorSettingsSchema(BaseModel):
    mode: str
    email: str
    polling: dict
    ranking: dict
    tracks: dict
    sources: dict
    preferences: dict
    presets: dict

