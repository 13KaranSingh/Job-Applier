from typing import Any

from packages.adapters.ats.greenhouse import GreenhouseAdapter


class LeverAdapter(GreenhouseAdapter):
    source_name = "Lever"
    source_slug = "lever"

    def extract_metadata(self, raw_job: dict[str, Any]) -> dict[str, Any]:
        return {"ats_type": "lever"}

