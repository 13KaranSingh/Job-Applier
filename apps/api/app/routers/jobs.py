from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from apps.api.app.deps import get_db
from apps.api.app.services.job_service import JobService
from packages.core.enums import SortMode

router = APIRouter(prefix="/jobs", tags=["jobs"])
service = JobService()


@router.get("")
def list_jobs(db: Session = Depends(get_db)) -> dict[str, list[dict]]:
    items = service.list_jobs(db)
    return {
        "items": [
            {
                "id": str(item.id),
                "company_name": item.company_name,
                "title_normalized": item.title_normalized,
                "location_normalized": item.location_normalized,
                "status": item.status,
                "first_seen_at": item.first_seen_at,
                "posted_at_source": item.posted_at_source,
                "apply_url": item.apply_url,
            }
            for item in items
        ]
    }


@router.get("/top")
def list_top_jobs(
    db: Session = Depends(get_db),
    sort_mode: SortMode = Query(default=SortMode.BEST_OVERALL),
    track: str | None = Query(default=None),
    remote_only: bool = Query(default=False),
    auto_apply_only: bool = Query(default=False),
) -> dict[str, list[dict]]:
    return {
        "items": service.list_top_jobs(
            db,
            sort_mode=sort_mode,
            track=track,
            remote_only=remote_only,
            auto_apply_only=auto_apply_only,
        )
    }


@router.get("/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)) -> dict:
    job = service.get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": str(job.id),
        "company_name": job.company_name,
        "title_raw": job.title_raw,
        "title_normalized": job.title_normalized,
        "description_text": job.description_text,
        "apply_url": job.apply_url,
    }


@router.post("/{job_id}/rerank")
def rerank_job(job_id: str, db: Session = Depends(get_db)) -> dict[str, str]:
    result = service.rerank_job(db, job_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return result


@router.post("/{job_id}/apply")
def apply_job(job_id: str, db: Session = Depends(get_db)) -> dict[str, str]:
    result = service.apply_job(db, job_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return result
