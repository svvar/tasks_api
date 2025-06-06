from datetime import datetime, date

from pydantic import BaseModel, ConfigDict

from database.enums.task_enums import TaskStatus


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    due_date: date | None = None
    status: TaskStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserInfoResponse(BaseModel):
    id: int
    email: str
    first_name: str | None = None
    last_name: str | None = None
    registration_date: datetime

    model_config = ConfigDict(from_attributes=True)