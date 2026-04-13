from operator import itemgetter
from typing import Any

from packages.core.enums import SortMode


def sort_top_jobs(items: list[dict[str, Any]], sort_mode: SortMode = SortMode.BEST_OVERALL) -> list[dict[str, Any]]:
    if sort_mode == SortMode.HIGHEST_PAY:
        return sorted(items, key=itemgetter("compensation_score", "total_score"), reverse=True)
    if sort_mode == SortMode.HIGHEST_PRESTIGE:
        return sorted(items, key=itemgetter("prestige_score", "total_score"), reverse=True)
    if sort_mode == SortMode.BEST_QUANT:
        return sorted(items, key=itemgetter("quant_score", "total_score"), reverse=True)
    if sort_mode == SortMode.BEST_SWE:
        return sorted(items, key=itemgetter("swe_score", "total_score"), reverse=True)
    if sort_mode == SortMode.FASTEST_APPLY:
        return sorted(items, key=itemgetter("automation_readiness_score", "recency_score"), reverse=True)
    if sort_mode == SortMode.BEST_REMOTE:
        return sorted(items, key=itemgetter("location_fit_score", "total_score"), reverse=True)
    return sorted(items, key=itemgetter("total_score", "company_priority_score"), reverse=True)

