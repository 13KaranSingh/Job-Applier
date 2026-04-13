from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from apps.api.app.deps import get_db
from apps.api.app.services.profile_service import ProfileService

router = APIRouter(prefix="/resumes", tags=["resumes"])
service = ProfileService()


@router.get("")
def list_resumes(db: Session = Depends(get_db)) -> dict[str, list[dict]]:
    items = service.list_resumes(db)
    return {
        "items": [
            {
                "id": str(item.id),
                "variant_name": item.variant_name,
                "file_path": item.file_path,
                "active": item.active,
                "metadata_json": item.metadata_json,
            }
            for item in items
        ]
    }


@router.post("")
def create_resume(payload: dict = Body(...), db: Session = Depends(get_db)) -> dict[str, str]:
    resume = service.create_resume(db, payload)
    return {"id": str(resume.id), "status": "created"}
