from fastapi import APIRouter

from apps.api.app.services.settings_service import SettingsService

router = APIRouter(prefix="/settings", tags=["settings"])
service = SettingsService()


@router.get("")
def get_settings_snapshot() -> dict[str, dict]:
    return {"settings": service.get_snapshot()}

