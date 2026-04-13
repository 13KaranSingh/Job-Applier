def build_daily_digest(stats: dict) -> str:
    return (
        f"Jobs discovered today: {stats.get('jobs_discovered', 0)}\n"
        f"Applications submitted today: {stats.get('applications_submitted', 0)}\n"
        f"Failures today: {stats.get('applications_failed', 0)}"
    )

