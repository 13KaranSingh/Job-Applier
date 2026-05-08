from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, HTTPException

from apps.worker.tasks.notifications import send_top_job_alerts
from apps.worker.tasks.polling import poll_sources
from apps.worker.tasks.profile import seed_profile
from apps.worker.tasks.ranking import decide_actions, rank_jobs
from apps.worker.tasks.sheets_sync import sync_google_sheets

router = APIRouter(prefix="/ops", tags=["ops"])


def _run_full_refresh() -> dict[str, Any]:
    profile = seed_profile()
    polling = poll_sources()
    ranking = rank_jobs()
    decisions = decide_actions()
    exports = sync_google_sheets()
    return {
        "profile": profile,
        "polling": polling,
        "ranking": ranking,
        "decisions": decisions,
        "exports": exports,
    }


OPERATIONS: dict[str, Callable[[], dict[str, Any] | str]] = {
    "seed-profile": seed_profile,
    "poll": poll_sources,
    "rank": rank_jobs,
    "decide": decide_actions,
    "export-csv": sync_google_sheets,
    "send-alerts": send_top_job_alerts,
    "full-refresh": _run_full_refresh,
}


@router.post("/{operation}")
def run_operation(operation: str) -> dict[str, Any]:
    runner = OPERATIONS.get(operation)
    if runner is None:
        raise HTTPException(status_code=404, detail="Unknown operation")
    result = runner()
    return {"operation": operation, "result": result}
