from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.types import Username, Password


class UserCreate(BaseModel):
    email: EmailStr
    username: Username
    password: Password


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: Username | None = None
    password: Password | None = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: Username
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}
