# Define the data structure for the incoming request
from datetime import date, timedelta
from pydantic import BaseModel, EmailStr, HttpUrl, field_validator
from pydantic_core.core_schema import ValidationInfo


class LogRequest(BaseModel):
    jira_domain: HttpUrl
    email: EmailStr
    api_token: str
    start_date: date
    end_date: date

    @field_validator("end_date", mode="after")
    def validate_date_range(cls, value: date, info: ValidationInfo):
        start_date = info.data.get("start_date")

        if start_date:
            if value < start_date:
                raise ValueError("End date must be after or the same as Start date")

            date_diff = value - start_date
            if date_diff > timedelta(days=31):
                raise ValueError(
                    "Start date and End date must be no more than one month apart"
                )
        return value
