from packages.sheets.mappers import top_jobs_row


def build_top_jobs_payload(jobs: list[dict], scores: dict[str, dict]) -> list[dict]:
    rows: list[dict] = []
    for job in jobs:
        score = scores.get(job["id"])
        if score and score["total_score"] >= 70 and job.get("status") == "active":
            rows.append(top_jobs_row(job, score))
    return rows

