from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.log_request import LogRequest
from app.service.jira_service import JiraService, get_jira_service

api_router = APIRouter(prefix="/api")


@api_router.get("/health", response_class=JSONResponse, status_code=200)
async def health_check():
    return {"status": "ok"}


@api_router.post("/logged-time")
async def get_logged_time(
    *, jira_service: JiraService = Depends(get_jira_service), request: LogRequest
):
    try:
        current_account_id = jira_service.get_account_id(
            request.jira_domain, request.email, request.api_token
        )
        issues = jira_service.get_issues(
            request.jira_domain,
            request.email,
            request.api_token,
            request.start_date,
            request.end_date,
        )

        total_logged_seconds = 0
        logged_time_details = defaultdict(
            lambda: {"time_spent_seconds": 0, "details": []}
        )

        for issue in issues:
            issue_key = issue["key"]
            issue_summary = issue["fields"]["summary"]
            worklogs = jira_service.get_worklogs(
                request.jira_domain, request.email, request.api_token, issue_key
            )

            for log in worklogs:
                account_id = log["author"]["accountId"]
                logged_date = log["started"][:10]
                logged_datetime = datetime.strptime(logged_date, "%Y-%m-%d").date()
                time_spent_seconds = log["timeSpentSeconds"]

                if (
                    account_id == current_account_id
                    and request.start_date <= logged_datetime <= request.end_date
                ):
                    start_time = datetime.strptime(
                        log["started"], "%Y-%m-%dT%H:%M:%S.%f%z"
                    )
                    end_time = start_time + timedelta(seconds=time_spent_seconds)

                    logged_time_details[logged_date]["details"].append(
                        {
                            "issue": issue_key,
                            "summary": issue_summary,
                            "date": logged_date,
                            "start_time": start_time.strftime("%H:%M"),
                            "end_time": end_time.strftime("%H:%M"),
                            "time_spent_hours": round(time_spent_seconds / 3600, 2),
                        }
                    )
                    logged_time_details[logged_date][
                        "time_spent_seconds"
                    ] += time_spent_seconds
                    total_logged_seconds += time_spent_seconds

        return {
            "logged_time_details": logged_time_details,
            "total_logged_hours": round(total_logged_seconds / 3600, 2),
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
