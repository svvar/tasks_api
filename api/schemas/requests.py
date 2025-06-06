from datetime import datetime, date

from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator

from database.enums.task_enums import TaskStatus


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: SecretStr

    @field_validator('password')
    @classmethod
    def check_password(cls, v):
        secret_value = v.get_secret_value()
        if len(secret_value) < 8:
            raise ValueError("Password should be at least 8 characters long.")
        if not any(char.isdigit() for char in secret_value) or not any(char.isupper() for char in secret_value) or not any(char.islower() for char in secret_value):
            raise ValueError("Password should contain at least one digit, one uppercase letter, and one lowercase letter.")
        return v

class CreateUserRequest(LoginUserRequest):
    first_name: str | None = None
    last_name: str | None = None


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1)
    description: str | None = None
    due_date: date | None = None
    status: TaskStatus = TaskStatus.PENDING

class UpdateTaskRequest(CreateTaskRequest):
    title: str = Field(None, min_length=1)