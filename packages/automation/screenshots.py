from pathlib import Path


def screenshot_path(storage_root: str, application_id: str, suffix: str) -> Path:
    return Path(storage_root) / "screenshots" / f"{application_id}-{suffix}.png"

