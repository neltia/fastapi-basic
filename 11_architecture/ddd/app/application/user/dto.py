from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: bool = True


class UserCreateDTO(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdateDTO(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserDTO(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: list[UserDTO]
    total: int
    page: int
    per_page: int


class UserDetailResponse(UserDTO):
    pass


class UserDeleteResponse(BaseModel):
    message: str
    deleted_user_id: int
