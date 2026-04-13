from fastapi import APIRouter

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.get("")
def list_resumes() -> dict[str, list]:
    return {"items": []}


@router.post("")
def create_resume() -> dict[str, str]:
    return {"status": "created"}

