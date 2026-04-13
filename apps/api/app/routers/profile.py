from fastapi import APIRouter

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("")
def get_profile() -> dict[str, dict]:
    return {"profile": {}}


@router.put("")
def update_profile() -> dict[str, str]:
    return {"status": "updated"}

