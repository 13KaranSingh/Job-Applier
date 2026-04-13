from fastapi import FastAPI

from apps.api.app.routers import (
    analytics,
    answers,
    applications,
    health,
    jobs,
    profile,
    resumes,
    settings,
    sources,
)
from packages.db.bootstrap import create_all_tables

app = FastAPI(title="Job Bot API", version="0.1.0")

app.include_router(health.router)
app.include_router(sources.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(analytics.router)
app.include_router(profile.router)
app.include_router(answers.router)
app.include_router(resumes.router)
app.include_router(settings.router)


@app.on_event("startup")
def on_startup() -> None:
    create_all_tables()
