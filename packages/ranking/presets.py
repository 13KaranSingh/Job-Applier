from packages.core.enums import SortMode

SORT_MODE_FIELDS = {
    SortMode.BEST_OVERALL: ["total_score", "posted_at_source"],
    SortMode.HIGHEST_PAY: ["compensation_score", "total_score"],
    SortMode.HIGHEST_PRESTIGE: ["prestige_score", "total_score"],
    SortMode.BEST_QUANT: ["quant_score", "total_score"],
    SortMode.BEST_SWE: ["swe_score", "total_score"],
    SortMode.FASTEST_APPLY: ["automation_readiness_score", "recency_score"],
    SortMode.BEST_REMOTE: ["location_fit_score", "total_score"],
}

