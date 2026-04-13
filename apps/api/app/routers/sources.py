from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.api.app.deps import get_db
from apps.api.app.services.source_service import SourceService

router = APIRouter(prefix="/sources", tags=["sources"])
service = SourceService()


@router.get("")
def list_sources(db: Session = Depends(get_db)) -> dict[str, list[dict]]:
    items = service.list_sources(db)
    return {
        "items": [
            {
                "id": str(item.id),
                "name": item.name,
                "slug": item.slug,
                "enabled": item.enabled,
                "source_type": item.source_type,
                "priority_weight": item.priority_weight,
                "polling_interval_seconds": item.polling_interval_seconds,
                "supports_auto_apply": item.supports_auto_apply,
                "config_json": item.config_json,
            }
            for item in items
        ]
    }


@router.post("/seed")
def seed_sources(db: Session = Depends(get_db)) -> dict[str, int]:
    return {"created": service.seed_defaults(db)}


@router.post("/{source_id}/enable")
def enable_source(source_id: str, db: Session = Depends(get_db)) -> dict[str, str]:
    source = service.set_enabled(db, source_id, True)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"source_id": source_id, "status": "enabled"}


@router.post("/{source_id}/disable")
def disable_source(source_id: str, db: Session = Depends(get_db)) -> dict[str, str]:
    source = service.set_enabled(db, source_id, False)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"source_id": source_id, "status": "disabled"}
