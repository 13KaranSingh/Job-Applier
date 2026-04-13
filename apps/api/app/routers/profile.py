from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from apps.api.app.deps import get_db
from apps.api.app.services.profile_service import ProfileService

router = APIRouter(prefix="/profile", tags=["profile"])
service = ProfileService()


@router.get("")
def get_profile(db: Session = Depends(get_db)) -> dict[str, dict | None]:
    profile = service.get_profile(db)
    return {"profile": profile.profile_json if profile else None}


@router.put("")
def update_profile(payload: dict = Body(...), db: Session = Depends(get_db)) -> dict[str, dict]:
    profile = service.upsert_profile(db, payload)
    return {"profile": profile.profile_json}
