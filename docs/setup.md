# Setup

## Local Stack

1. Copy `.env.example` to `.env`.
2. Keep `.env`, `config/local/profile.json`, and resume PDFs under `storage/resumes/` local only.
3. Install Python 3.12, PostgreSQL, Redis, and Node locally, or use Docker for infra.
4. Create the Python env and install dependencies:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

5. Install dashboard dependencies:

```bash
cd apps/dashboard
npm install
cd ../..
```

6. Start Postgres and Redis.
7. Start the API:

```bash
.venv/bin/uvicorn apps.api.app.main:app --host 127.0.0.1 --port 8000
```

8. Start the dashboard:

```bash
cd apps/dashboard
npm run dev
```

9. Open `http://localhost:3000` and use `Overview -> Full Refresh`.

## Daily Operator Flow

1. Seed the local profile and resume assets through `Full Refresh`.
2. Configure live sources in the Sources page with `greenhouse_token`, `lever_slug`, or `career_url`.
3. Run `Poll Sources`, `Rank Jobs`, and `Healthcheck` after source changes.
4. Review `Top Jobs`, then use manual handoff or guarded auto-apply.
5. Export CSV trackers from the dashboard when needed.
