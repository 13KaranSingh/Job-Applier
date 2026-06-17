from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.api.app.deps import get_db
from apps.api.app.services.application_service import ApplicationService

router = APIRouter(prefix="/applications", tags=["applications"])
service = ApplicationService()


@router.get("")
def list_applications(db: Session = Depends(get_db)) -> dict[str, list[dict]]:
    items = service.list_applications(db)
    return {
        "items": [
            {
                "id": str(item.id),
                "job_id": str(item.job_id),
                "status": item.status,
                "application_mode": item.application_mode,
                "resume_variant": item.resume_variant,
                "submitted_at": item.submitted_at,
                "company_name": job.company_name,
                "title_normalized": job.title_normalized,
                "location_normalized": job.location_normalized,
                "apply_url": job.apply_url,
                "notes": item.notes,
                "failure_code": item.failure_code,
                "failure_stage": item.failure_stage,
            }
            for item, job in items
        ]
    }


@router.get("/{application_id}")
def get_application(application_id: str, db: Session = Depends(get_db)) -> dict:
    item = service.get_application(db, application_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "id": str(item.id),
        "job_id": item.job_id,
        "status": item.status,
        "notes": item.notes,
        "failure_code": item.failure_code,
    }


@router.post("/{application_id}/retry")
def retry_application(application_id: str, db: Session = Depends(get_db)) -> dict[str, str]:
    item = service.retry_application(db, application_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"application_id": application_id, "status": item.status}
