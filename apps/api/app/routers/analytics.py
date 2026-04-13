from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary")
def get_summary() -> dict[str, dict]:
    return {"summary": {}}

