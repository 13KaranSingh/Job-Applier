def top_jobs_row(job: dict, score: dict) -> dict:
    return {
        "internal_job_id": job["id"],
        "company": job["company_name"],
        "title": job["title_normalized"],
        "location": job["location_normalized"],
        "source_name": job["source_name"],
        "posted_at_source": job.get("posted_at_source"),
        "discovered_at": job.get("first_seen_at"),
        "total_score": score["total_score"],
        "top_match_reasons": ", ".join(score.get("explanations", [])),
        "auto_apply_supported": job.get("auto_apply_supported", False),
        "current_status": job.get("status", "new"),
        "action_link": job.get("apply_url"),
    }

