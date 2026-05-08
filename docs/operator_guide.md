# Operator Guide

Use `config/operator.yaml` for ranking thresholds, source exclusions, polling cadence, preferred
locations, and mode selection between balanced, SWE-priority, and quant-priority operation.

## Daily Local Flow

1. Start Postgres, Redis, FastAPI, and the dashboard.
2. Open the dashboard at `http://localhost:3000`.
3. Use Overview → `Full Refresh` to seed profile data, poll sources, rank jobs, and export CSV trackers.
4. Review Top Jobs, then use Apply for manual handoff or `Auto Apply` only when source confidence is high.
5. Download tracker CSVs from the dashboard or read them from `storage/exports/`.

## Adding Live Sources

Use the Sources page to add:

- Greenhouse boards with `greenhouse_token`
- Lever boards with `lever_slug`
- Generic careers pages with `career_url` when they expose JSON-LD `JobPosting` data

LinkedIn and Workday remain excluded. Do not add them as sources.

## Safety Rules

- `.env`, `config/local/profile.json`, and PDFs under `storage/resumes/` are local-only and ignored by git.
- Yahoo alerts are sent only when `YAHOO_SMTP_APP_PASSWORD` is configured.
- Re-running apply actions is idempotent per job; existing application records are reused.
- Top-job alert notifications are suppressed per job/event key for 24 hours by default.
