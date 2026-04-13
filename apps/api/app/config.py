from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = Field(default="development", alias="APP_ENV")
    database_url: str = Field(alias="DATABASE_URL")
    redis_url: str = Field(alias="REDIS_URL")
    google_sheets_credentials: str = Field(alias="GOOGLE_SHEETS_CREDENTIALS")
    yahoo_smtp_username: str = Field(alias="YAHOO_SMTP_USERNAME")
    yahoo_smtp_app_password: str = Field(alias="YAHOO_SMTP_APP_PASSWORD")
    encryption_key: str = Field(alias="ENCRYPTION_KEY")
    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")
    storage_root: str = Field(default="storage", alias="STORAGE_ROOT")
    operator_config_path: str = Field(default="config/operator.yaml", alias="OPERATOR_CONFIG_PATH")
    playwright_headless: bool = Field(default=True, alias="PLAYWRIGHT_HEADLESS")


@lru_cache
def get_settings() -> Settings:
    return Settings()

