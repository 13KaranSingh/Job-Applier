from fastapi import APIRouter

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("")
def list_applications() -> dict[str, list]:
    return {"items": []}


@router.get("/{application_id}")
def get_application(application_id: str) -> dict[str, str]:
    return {"application_id": application_id}


@router.post("/{application_id}/retry")
def retry_application(application_id: str) -> dict[str, str]:
    return {"application_id": application_id, "status": "queued"}

