# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jira Worklog Extractor is a FastAPI web application that retrieves and displays time logged in Jira worklogs within a specified date range. It provides a browser-based dashboard for tracking utilization against an 8-hour/day target.

## Tech Stack

- **Backend:** FastAPI with Uvicorn
- **HTTP Client:** httpx (async, replaced requests)
- **Frontend:** Vanilla HTML/JS with Tailwind CSS (served statically)
- **Package Manager:** uv (replaced pip)
- **Validation:** Pydantic v2
- **Deployment:** Docker (multi-stage build, Alpine-based)

## Commands

### Setup & Development

```bash
# Install dependencies (creates/updates .venv)
uv sync

# Run the API server
uv run python -m app.main

# Or run directly via uvicorn
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build image
docker build . -t jira-worklog:1.0

# Run container
docker run -p 8000:8000 jira-worklog:1.0
```

### Testing

```bash
# No formal test suite exists; manual testing via UI or curl
curl -X POST http://localhost:8000/api/logged-time \
  -H "Content-Type: application/json" \
  -d '{"jira_domain":"https://your-org.atlassian.net","email":"user@example.com","api_token":"token","start_date":"2026-03-01","end_date":"2026-03-28"}'
```

## Code Architecture

### Entry Points

- **`app/main.py`** - FastAPI app initialization with CORS middleware
- **`app/console.py`** - CLI script for manual Jira queries (legacy, not used by API)

### API Structure

```
/api/health           → GET  health check
/api/logged-time      → POST query Jira worklogs
```

### Service Layer

- **`app/service/jira_service.py`** - `JiraService` class with Jira API methods:
  - `get_account_id()` - Look up user ID from email
  - `get_issues()` - JQL search for worklog entries
  - `get_worklogs()` - Fetch worklogs for specific issue
  - Uses `@lru_cache()` singleton via `get_jira_service()` dependency

### Request Validation

- **`app/schemas/log_request.py`** - `LogRequest` Pydantic model:
  - Fields: `jira_domain`, `email`, `api_token`, `start_date`, `end_date`
  - Validates: end_date >= start_date, range <= 31 days, `jira_domain` trailing slash stripped

### Frontend

- **`static/index.html`** - Single-page app with:
  - LocalStorage for credentials (30-day expiry) and start date
  - Dashboard with utilization metrics vs 8h/day target
  - API URL: `https://jira-worklog-api.onrender.com/api` (hardcoded)

## Environment Variables

Create `.env` with:
```env
JIRA_DOMAIN=https://your-org.atlassian.net
EMAIL=user@example.com
API_TOKEN=your-api-token
```

## Key Design Decisions

1. **No backend database** - Frontend stores credentials in browser localStorage
2. **Date range limit** - Max 31 days enforced by Pydantic validator
3. **Jira API** - Uses JQL `worklogAuthor = currentUser() AND worklogDate >= "{start}" AND worklogDate <= "{end}"`
4. **Async HTTP client** - All `JiraService` methods use `httpx.AsyncClient` so the event loop is never blocked
5. **HttpUrl normalization** - `jira_domain` is validated then cast to `str` with trailing slash stripped (Pydantic v2 `HttpUrl` always appends one)
6. **Docker multi-stage build** - Uses `uv` for dependency resolution, minimal Alpine runtime
7. **Hardcoded deployment URL** - Frontend points to Render deployment (`onrender.com`)

## Working Directories

- Code lives under `app/`
- Static frontend assets in `static/`
- Virtual environment created at `.venv/` by uv
- Docker builds from root with COPY operations
