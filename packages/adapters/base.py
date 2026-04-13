from abc import ABC, abstractmethod
from typing import Any

from packages.schemas.job import JobSchema


class BaseSourceAdapter(ABC):
    source_name: str
    source_slug: str

    @abstractmethod
    async def discover_jobs(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def normalize_job(self, raw_job: dict[str, Any]) -> JobSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_job_detail(self, job_ref: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def supports_auto_apply(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def apply(self, job: JobSchema, profile: dict[str, Any], resume_variant: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def healthcheck(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def extract_metadata(self, raw_job: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

