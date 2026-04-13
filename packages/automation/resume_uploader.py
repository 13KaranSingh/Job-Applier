from pathlib import Path


def resolve_resume_path(storage_root: str, variant_name: str) -> Path:
    return Path(storage_root) / "resumes" / variant_name

