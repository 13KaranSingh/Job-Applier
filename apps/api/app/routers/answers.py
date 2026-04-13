from fastapi import APIRouter

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("")
def list_answers() -> dict[str, list]:
    return {"items": []}


@router.post("")
def create_answer() -> dict[str, str]:
    return {"status": "created"}


@router.put("/{answer_id}")
def update_answer(answer_id: str) -> dict[str, str]:
    return {"answer_id": answer_id, "status": "updated"}

