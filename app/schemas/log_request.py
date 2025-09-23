# Define the data structure for the incoming request
from pydantic import BaseModel


class LogRequest(BaseModel):
    jira_domain: str
    email: str
    api_token: str
    start_date: str
    end_date: str
