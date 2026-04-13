from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from apps.api.app.deps import get_db
from apps.api.app.services.profile_service import ProfileService

router = APIRouter(prefix="/answers", tags=["answers"])
service = ProfileService()


@router.get("")
def list_answers(db: Session = Depends(get_db)) -> dict[str, list[dict]]:
    items = service.list_answers(db)
    return {
        "items": [
            {
                "id": str(item.id),
                "answer_key": item.answer_key,
                "category": item.category,
                "prompt_patterns": item.prompt_patterns_json,
                "answer_text": item.answer_text,
                "requires_human_review": item.requires_human_review,
                "active": item.active,
            }
            for item in items
        ]
    }


@router.post("")
def create_answer(payload: dict = Body(...), db: Session = Depends(get_db)) -> dict[str, str]:
    answer = service.create_answer(db, payload)
    return {"id": str(answer.id), "status": "created"}


@router.put("/{answer_id}")
def update_answer(answer_id: str, payload: dict = Body(...), db: Session = Depends(get_db)) -> dict[str, str]:
    answer = service.update_answer(db, answer_id, payload)
    if answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return {"answer_id": answer_id, "status": "updated"}
