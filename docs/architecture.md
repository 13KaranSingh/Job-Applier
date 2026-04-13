# Architecture

The platform is structured as a Python-first monorepo with shared packages for schemas, ranking,
adapters, notifications, sheets sync, and automation. FastAPI exposes operator APIs, Celery runs
polling and application workflows, and the dashboard consumes the internal API.

