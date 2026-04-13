from packages.core.enums import SortMode
from packages.ranking.queue import sort_top_jobs


def test_sort_top_jobs_by_highest_prestige() -> None:
    items = [
        {"total_score": 70, "prestige_score": 4, "company_priority_score": 5},
        {"total_score": 65, "prestige_score": 8, "company_priority_score": 5},
    ]
    sorted_items = sort_top_jobs(items, SortMode.HIGHEST_PRESTIGE)
    assert sorted_items[0]["prestige_score"] == 8
