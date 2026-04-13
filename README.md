# Job Application Automation Platform

Python-first monorepo for discovery, ranking, review, and controlled automation of SWE and quant job applications.

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Redis
- Celery
- Playwright
- Next.js 15 + TypeScript
- Tailwind CSS

## Services

- `apps/api`: internal API and operator service
- `apps/worker`: Celery workers and schedules
- `apps/dashboard`: operator dashboard
- `packages/*`: shared business logic, schemas, adapters, ranking, notifications, sheets, and profile modules

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

## MVP Notes

- LinkedIn is excluded
- Workday flows are excluded
- Google Sheets remains a projection; PostgreSQL is source of truth
- Auto-apply is gated behind confidence and friction rules

