from celery import shared_task

from pathlib import Path

from apps.api.app.config import get_settings


@shared_task(name="apps.worker.tasks.cleanup.cleanup_old_artifacts")
def cleanup_old_artifacts() -> dict[str, int]:
    settings = get_settings()
    removed = 0
    for folder in ["screenshots", "html_snapshots"]:
        target = Path(settings.storage_root) / folder
        if not target.exists():
            continue
        for item in target.iterdir():
            if item.name == ".gitkeep":
                continue
            if item.is_file():
                item.unlink()
                removed += 1
    return {"removed": removed}
