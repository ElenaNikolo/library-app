from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(max_length=120)
    password: str = Field(min_length=8)
    role: Literal[UserRole.LIBRARIAN, UserRole.ADMIN]


class UserUpdate(BaseModel):
    role: UserRole
    is_active: bool


class UserListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool
