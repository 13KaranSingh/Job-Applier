from datetime import UTC, datetime


def score_recency(posted_at: datetime | None, now: datetime | None = None) -> float:
    if posted_at is None:
        return 0.0
    current = now or datetime.now(UTC)
    age_hours = max((current - posted_at).total_seconds() / 3600, 0)
    if age_hours <= 2:
        return 15.0
    if age_hours <= 6:
        return 13.0
    if age_hours <= 12:
        return 11.0
    if age_hours <= 24:
        return 9.0
    if age_hours <= 72:
        return 6.0
    if age_hours <= 168:
        return 3.0
    return 0.0


def bounded(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))

