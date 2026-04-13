from fastapi import APIRouter

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("")
def list_sources() -> dict[str, list]:
    return {"items": []}


@router.post("/{source_id}/enable")
def enable_source(source_id: str) -> dict[str, str]:
    return {"source_id": source_id, "status": "enabled"}


@router.post("/{source_id}/disable")
def disable_source(source_id: str) -> dict[str, str]:
    return {"source_id": source_id, "status": "disabled"}

