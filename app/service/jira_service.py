from functools import lru_cache
from fastapi import HTTPException
import httpx


class JiraService:
    def __init__(self):
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def get_account_id(self, jira_domain: str, email: str, api_token: str) -> str:
        user_url = f"{jira_domain}/rest/api/3/user/search"
        params = {"query": email}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                user_url,
                headers=self.headers,
                auth=(email, api_token),
                params=params,
            )

        if response.status_code == 200:
            return response.json()[0]["accountId"]
        raise HTTPException(
            status_code=response.status_code,
            detail="Error fetching account id. Check your credentials.",
        )

    async def get_issues(
        self, jira_domain: str, email: str, api_token: str, start_date: str, end_date: str
    ) -> list:
        search_url = f"{jira_domain}/rest/api/3/search/jql"
        jql_query = f'worklogAuthor = currentUser() AND worklogDate >= "{start_date}" AND worklogDate <= "{end_date}"'
        params = {"jql": jql_query, "fields": ["summary"], "maxResults": 100}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                search_url,
                headers=self.headers,
                auth=(email, api_token),
                params=params,
            )

        if response.status_code == 200:
            return response.json().get("issues", [])
        raise HTTPException(
            status_code=response.status_code,
            detail="Error fetching issues. Check your date range or JQL query.",
        )

    async def get_worklogs(self, jira_domain: str, email: str, api_token: str, issue_key: str) -> list:
        worklog_url = f"{jira_domain}/rest/api/3/issue/{issue_key}/worklog"
        async with httpx.AsyncClient() as client:
            response = await client.get(
                worklog_url, headers=self.headers, auth=(email, api_token)
            )

        if response.status_code == 200:
            return response.json().get("worklogs", [])
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error fetching worklogs for {issue_key}.",
        )


# Define Dependencies
# This caches the service instance for the app's lifetime
@lru_cache()
def get_jira_service() -> JiraService:
    return JiraService()
