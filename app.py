import os
import requests
from collections import defaultdict
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # Take environment variables from .env

# Jira credentials
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("API_TOKEN")

# Headers
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


# Get account id
def get_account_id():
    USER_URL = f"{JIRA_DOMAIN}/rest/api/3/user/search"

    params = {"query": EMAIL}

    response = requests.get(
        USER_URL, headers=HEADERS, auth=(EMAIL, API_TOKEN), params=params
    )

    if response.status_code == 200:
        return response.json()[0]["accountId"]
    else:
        print("Error fetching account id:", response.text)
        return []


# Fetch issues where the user logged time
def get_issues(start_date: str, end_date: str):
    SEARCH_URL = f"{JIRA_DOMAIN}/rest/api/2/search"

    # JQL query to find issues where you logged time in the given range
    JQL_QUERY = f'worklogAuthor = currentUser() AND worklogDate >= "{start_date}" AND worklogDate <= "{end_date}"'

    params = {
        "jql": JQL_QUERY,
        "fields": ["summary"],  # Fetch only necessary fields
        "maxResults": 100,
    }

    response = requests.get(
        SEARCH_URL, headers=HEADERS, auth=(EMAIL, API_TOKEN), params=params
    )

    if response.status_code == 200:
        return response.json()["issues"]
    else:
        print("Error fetching issues:", response.text)
        return []


# Fetch worklogs for each issue
def get_worklogs(issue_key: str):
    WORKLOG_URL = f"{JIRA_DOMAIN}/rest/api/2/issue/{issue_key}/worklog"

    response = requests.get(WORKLOG_URL, headers=HEADERS, auth=(EMAIL, API_TOKEN))

    if response.status_code == 200:
        return response.json()["worklogs"]
    else:
        print(f"Error fetching worklogs for {issue_key}:", response.text)
        return []


# Process worklogs and filter by user & date range
def fetch_logged_time(start_date: str, end_date: str):
    # Get account id
    current_account_id = get_account_id()

    # Get issues
    issues = get_issues(start_date, end_date)

    total_logged_seconds = 0
    logged_time_details = defaultdict(lambda: {"time_spent_seconds": 0, "details": []})

    for issue in issues:
        issue_key = issue["key"]
        issue_summary = issue["fields"]["summary"]
        worklogs = get_worklogs(issue_key)

        for log in worklogs:
            account_id = log["author"]["accountId"]
            logged_date = log["started"][:10]
            time_spent_seconds = log["timeSpentSeconds"]

            if (
                account_id == current_account_id
                and start_date <= logged_date <= end_date
            ):
                # Parse the datetime and timezone offset
                start_time = datetime.strptime(log["started"], "%Y-%m-%dT%H:%M:%S.%f%z")
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

    # Display result
    print("\n--- Logged Time in Jira ---")
    for logged_date in sorted(logged_time_details.keys()):
        time_logged_hrs = logged_time_details[logged_date]["time_spent_seconds"] / 3600
        print(f"\n{logged_date} - Time logged: {time_logged_hrs:.2f} hours")

        for log in sorted(
            logged_time_details[logged_date]["details"],
            key=lambda item: item["start_time"],
        ):
            print(
                f"{log['date']} | {log['time_spent_hours']:<4} hrs | {log['issue']} | ({log['start_time']} - {log['end_time']}) | {log['summary'][:50]}..."
            )

    print(f"\nTotal Time Logged: {total_logged_seconds / 3600:.2f} hours")


# Run the script
if __name__ == "__main__":
    start_date = "2025-01-01"
    end_date = "2025-01-30"

    fetch_logged_time(start_date, end_date)
