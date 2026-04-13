from celery import shared_task


@shared_task(name="apps.worker.tasks.ranking.rank_jobs")
def rank_jobs() -> str:
    return "queued"

