from fastapi import APIRouter

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
def list_jobs() -> dict[str, list]:
    return {"items": []}


@router.get("/top")
def list_top_jobs() -> dict[str, list]:
    return {"items": []}


@router.get("/{job_id}")
def get_job(job_id: str) -> dict[str, str]:
    return {"job_id": job_id}


@router.post("/{job_id}/rerank")
def rerank_job(job_id: str) -> dict[str, str]:
    return {"job_id": job_id, "status": "queued"}


@router.post("/{job_id}/apply")
def apply_job(job_id: str) -> dict[str, str]:
    return {"job_id": job_id, "status": "queued"}

