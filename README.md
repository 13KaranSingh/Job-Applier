# Job Application Automation Platform

Python-first monorepo for continuously discovering, ranking, tracking, and selectively automating SWE and quant job applications.

## What This Repo Does

The platform is built around a fast discovery-to-decision loop:

1. Poll direct company boards, Greenhouse, Lever, and curated quant targets.
2. Normalize jobs into a canonical schema.
3. Deduplicate mirrored postings.
4. Score each job using freshness, fit, compensation, prestige, location, and automation readiness.
5. Decide whether to auto-apply, queue for review, alert only, or ignore.
6. Persist state in PostgreSQL.
7. Project key data into CSV tracker exports and email notifications.
8. Expose operator controls through FastAPI and the dashboard.

Hard constraints enforced by design:

- LinkedIn is excluded.
- Workday flows are excluded.
- Auto-apply is confidence-gated and selective.
- The database is the system of record.

## Repository Layout

```text
apps/
  api/        FastAPI service
  worker/     Celery workers and scheduled tasks
  dashboard/  Next.js operator UI
packages/
  adapters/   Source adapters and parsing utilities
  automation/ Browser/form automation primitives
  core/       Enums, constants, shared helpers
  db/         SQLAlchemy models, session, bootstrap, migrations
  notifications/
  profile/
  ranking/
  schemas/
  sheets/
  source_seeding/
config/
  operator.yaml
tests/
docs/
storage/
```

## Current Implementation Status

Implemented now:

- Monorepo scaffold and local Docker workflow
- FastAPI app and worker scaffold
- SQLAlchemy model set
- Alembic scaffold with initial revision placeholder
- Source seeding from company metadata
- Starter adapter framework for company, ATS, and generic JSON-LD careers pages
- Normalization, compensation parsing, canonical dedup key generation
- Ranking engine with SWE, quant, and balanced scoring
- Decision classification and top-job queue sorting
- DB-backed API routes for sources, jobs, applications, analytics, profile, answers, resumes, and ops
- Dashboard pages wired to live API data
- Dashboard actions for source management, rerank, manual apply, retry, CSV export, and pipeline runs
- CSV tracker exports for Applications, Top Jobs, Job Feed, and Failures
- Yahoo SMTP notification queue with duplicate suppression
- Idempotent manual handoff and auto-apply attempts
- Unit tests for ranking, queue sorting, dedup, source seeding, ATS adapters, generic adapter, and CSV sync

Still to finish for full production readiness:

- Complete Alembic revisions for every table
- More direct live adapters beyond ATS/generic careers ingestion
- Production-grade Playwright submission flows for supported companies
- Real Google Sheets client integration if you choose to add it later
- Full observability dashboards, retries, and artifact storage plumbing

## Scoring Model

The platform stores both blended and track-specific scoring.

Core blended score inputs:

- recency
- title fit
- seniority fit
- company priority
- prestige
- compensation
- location fit
- skills fit
- role family fit
- source quality
- automation readiness
- friction penalty
- exclusion penalty

Track-specific scoring:

- `swe_score`
- `quant_score`
- `interview_probability`

Balanced mode uses a blended score. SWE-priority mode favors SWE outcomes. Quant-priority mode favors quant outcomes.

## Quick Start

### 1. Configure environment

```bash
cp .env.example .env
```

Update at minimum:

- `DATABASE_URL`
- `REDIS_URL`
- `GOOGLE_SHEETS_CREDENTIALS`
- `YAHOO_SMTP_USERNAME`
- `YAHOO_SMTP_APP_PASSWORD`
- `ENCRYPTION_KEY`

### 2. Start the stack

```bash
docker compose up --build
```

Services:

- API: `http://localhost:8000`
- Dashboard: `http://localhost:3000`
- Postgres: `localhost:5432`
- Redis: `localhost:6379`

### 3. Seed default sources

```bash
curl -X POST http://localhost:8000/sources/seed
```

### 4. Run the pipeline

Open the dashboard Overview page and use:

- `Full Refresh`: seed local profile, poll sources, rank jobs, decide actions, export CSVs
- `Poll Sources`: pull fixture and configured live sources
- `Rank Jobs`: recompute scores
- `Auto Apply`: run the guarded auto-apply worker
- `Export CSV`: regenerate tracker exports
- `Send Alerts`: send queued top-job Yahoo alerts

Equivalent shell commands are still available:

```bash
python -c "from apps.worker.tasks.profile import seed_profile; print(seed_profile())"
python -c "from apps.worker.tasks.polling import poll_sources; print(poll_sources())"
python -c "from apps.worker.tasks.ranking import rank_jobs; print(rank_jobs())"
python -c "from apps.worker.tasks.sheets_sync import sync_google_sheets; print(sync_google_sheets())"
```

### Local profile and resumes

Personal profile data should live in `config/local/profile.json`. That path is ignored by git.

Resume PDFs should live in `storage/resumes/`. That directory ignores PDFs by default so resumes are not committed.

Seed your local profile and resume assets:

```bash
python -c "from apps.worker.tasks.profile import seed_profile; print(seed_profile())"
```

Auto-apply is controlled from the local profile under `application_preferences.auto_apply_enabled`.
Even when enabled, the worker still requires high score, supported automation, parser confidence, automation confidence, no exclusion penalty, and low friction before submitting.

### 5. Inspect health and sources

```bash
curl http://localhost:8000/health
curl http://localhost:8000/sources
```

## Operator Configuration

Primary runtime configuration lives in [`config/operator.yaml`](config/operator.yaml).

Key controls:

- operating mode: balanced, SWE-priority, quant-priority
- ranking thresholds
- polling cadence
- source exclusions
- preferred locations
- max role age

## Important API Endpoints

### Health and config

- `GET /health`
- `GET /settings`

### Sources

- `GET /sources`
- `POST /sources`
- `POST /sources/seed`
- `POST /sources/{id}/enable`
- `POST /sources/{id}/disable`
- `PUT /sources/{id}`

### Jobs

- `GET /jobs`
- `GET /jobs/top`
- `GET /jobs/{id}`
- `POST /jobs/{id}/rerank`
- `POST /jobs/{id}/apply`

### Applications

- `GET /applications`
- `GET /applications/{id}`
- `POST /applications/{id}/retry`

### Profile and answer library

- `GET /profile`
- `PUT /profile`
- `GET /answers`
- `POST /answers`
- `PUT /answers/{id}`
- `GET /resumes`
- `POST /resumes`

### Analytics

- `GET /analytics/summary`

### Operator pipeline

- `POST /ops/seed-profile`
- `POST /ops/poll`
- `POST /ops/rank`
- `POST /ops/decide`
- `POST /ops/auto-apply`
- `POST /ops/export-csv`
- `POST /ops/send-alerts`
- `POST /ops/full-refresh`

## Local Development

### Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### Dashboard

```bash
cd apps/dashboard
npm install
npm run dev
```

### Compile check

```bash
python3 -m compileall apps packages tests
```

## Database and Migrations

The FastAPI app currently creates tables on startup for development convenience.

Alembic files live in:

- `alembic.ini`
- `packages/db/migrations/env.py`
- `packages/db/migrations/versions/`

To generate or run migrations later:

```bash
alembic upgrade head
```

## Tracker Output

The human-readable tracker now supports CSV-first operation.

Generated files land in `storage/exports/`:

- `Applications.csv`
- `TopJobs.csv`
- `JobFeed.csv`
- `Failures.csv`

This keeps the operator loop simple and local. A Google Sheets sync layer can still be added later without changing the core ranking or decision pipeline.

## Yahoo Email

Outgoing mail is wired for Yahoo SMTP using:

- `YAHOO_SMTP_USERNAME`
- `YAHOO_SMTP_APP_PASSWORD`

Current default target:

- `karanvir_gurn@yahoo.com`

If the app password is unset or left as `change-me`, notifications are queued and marked sent logically without opening a live SMTP session. That keeps local development safe.

## Source Strategy

Primary targets:

- direct company boards
- Greenhouse
- Lever
- quant/trading firms
- startup watchlist companies

Initial seeded companies include:

- Google
- Amazon
- Jane Street
- Citadel Securities
- Stripe

Add real live sources from the dashboard Sources page:

- Greenhouse source: set `source_type=ats` and `greenhouse_token`
- Lever source: set `source_type=ats` and `lever_slug`
- Generic careers page: set `career_url` for a page with JSON-LD `JobPosting` data

The poller uses exact adapters first and falls back to the generic careers adapter when a source has `career_url`.

## Safety and Guardrails

- Never use LinkedIn as a source.
- Never support Workday application flows.
- Never fabricate years of experience or credentials.
- Never auto-apply to blacklisted companies.
- Never auto-apply when long-form unsupported prompts are required.
- Never auto-apply if parser or automation confidence is below threshold.

## Tests

Current tests cover:

- dedup key stability
- ranking behavior
- queue sorting
- source seeding behavior
- ATS and generic adapter parsing
- CSV tracker sync

Run:

```bash
pytest
```

## CI

GitHub Actions compile-check workflow:

- `.github/workflows/ci.yml`

## Remaining Production Work

1. Add full Alembic coverage for all tables.
2. Add more direct company adapters for target boards that do not expose Greenhouse, Lever, or JSON-LD.
3. Implement production Playwright form submission flows with screenshots, HTML snapshots, and confirmation detection.
4. Add background Celery beat schedules for continuous polling/ranking/exporting.
5. Add richer observability dashboards and notification retry/backoff.
