from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.api.app.deps import get_db
from apps.api.app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])
service = AnalyticsService()


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)) -> dict[str, dict]:
    return {"summary": service.get_summary(db)}
