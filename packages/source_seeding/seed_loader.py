import json
from pathlib import Path
from typing import Any


def load_default_companies() -> list[dict[str, Any]]:
    seed_path = Path(__file__).with_name("default_companies.json")
    return json.loads(seed_path.read_text())


def build_default_sources() -> list[dict[str, Any]]:
    company_sources = []
    for company in load_default_companies():
        company_sources.append(
            {
                "name": f"{company['company_name']} Careers",
                "slug": company["company_slug"],
                "source_type": "company",
                "enabled": True,
                "polling_interval_seconds": 180 if company["target_priority"] >= 95 else 600,
                "priority_weight": max(1, round(company["target_priority"] / 10)),
                "supports_auto_apply": False,
                "requires_login": False,
                "config_json": {
                    "company_type": company["company_type"],
                    "target_priority": company["target_priority"],
                    "prestige_tier": company["prestige_tier"],
                    "compensation_tier": company["compensation_tier"],
                    "role_bias": company["role_bias"],
                    "blacklisted": company["blacklisted"],
                },
            }
        )
    company_sources.extend(
        [
            {
                "name": "Greenhouse",
                "slug": "greenhouse",
                "source_type": "ats",
                "enabled": True,
                "polling_interval_seconds": 300,
                "priority_weight": 8,
                "supports_auto_apply": False,
                "requires_login": False,
                "config_json": {"ats_type": "greenhouse"},
            },
            {
                "name": "Lever",
                "slug": "lever",
                "source_type": "ats",
                "enabled": True,
                "polling_interval_seconds": 300,
                "priority_weight": 8,
                "supports_auto_apply": False,
                "requires_login": False,
                "config_json": {"ats_type": "lever"},
            },
        ]
    )
    return company_sources
