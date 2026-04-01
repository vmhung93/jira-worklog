---
name: Project Context — Post-Review State (2026-04-01)
description: Architectural decisions, resolved issues, and remaining patterns to watch after applying all code-review improvements
type: project
---

## Resolved Issues (applied 2026-04-01)

**Async HTTP** — All three `JiraService` methods are now `async def` using `httpx.AsyncClient`. The `requests` library has been removed from the project. Do not suggest reverting to synchronous HTTP.

**HttpUrl trailing slash** — A `normalize_jira_domain` validator in `LogRequest` strips the trailing slash Pydantic v2 injects from `HttpUrl`. The field is a plain `str` after validation, so f-string URL construction in the service layer is safe.

**CORS config** — `allow_credentials` is now `False`; `allow_methods` and `allow_headers` are narrowed to `["GET", "POST"]` and `["Content-Type"]`. The `allow_origins=["*"]` + `allow_credentials=True` combination is gone.

**Frontend localStorage hoist** — `credentials` is read and parsed once at the top of `displayDashboard` and passed into the `map()` loop via closure. No per-row storage reads.

**Frontend color map** — `createMetricCard` now uses a structured `{ text, bg, border }` object instead of positional `.split(' ')` indexing.

**Bare raise** — `except HTTPException as e: raise e` replaced with `except HTTPException: raise` in `api.py`.

**Type annotations** — `email` and `api_token` parameters in `get_issues` and `get_worklogs` now have `: str` annotations.

---

## Stable Patterns (do not flag)

**`@lru_cache()` on `get_jira_service()`** — intentional singleton. `JiraService` holds no per-request state; credentials are method arguments. Correct and expected.

**`start_time` sort in `api.py`** — sorts `"%H:%M"` strings. Works for same-day entries; would break across midnight, but that is acceptable for the current use case.

**Why:** Recorded to avoid re-raising already-fixed issues in future reviews and to preserve context on intentional design decisions.
**How to apply:** When reviewing service methods, CORS config, or JS frontend, check here first to avoid suggesting changes that were deliberately made or already applied.
