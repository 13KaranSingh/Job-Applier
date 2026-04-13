from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "poll-sources": {"task": "apps.worker.tasks.polling.poll_sources", "schedule": 180.0},
    "rank-jobs": {"task": "apps.worker.tasks.ranking.rank_jobs", "schedule": 240.0},
    "decide-actions": {"task": "apps.worker.tasks.ranking.decide_actions", "schedule": 300.0},
    "top-job-alerts": {"task": "apps.worker.tasks.notifications.send_top_job_alerts", "schedule": 600.0},
    "sync-google-sheets": {"task": "apps.worker.tasks.sheets_sync.sync_google_sheets", "schedule": 300.0},
    "healthcheck-sources": {"task": "apps.worker.tasks.healthchecks.healthcheck_sources", "schedule": 900.0},
    "daily-digest": {
        "task": "apps.worker.tasks.notifications.send_daily_digest",
        "schedule": crontab(hour=21, minute=0),
    },
}
