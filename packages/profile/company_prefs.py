from typing import Any


def metadata_by_company(companies: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {company["company_slug"]: company for company in companies}

