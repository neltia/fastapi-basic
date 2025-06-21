# app/api/v1/endpoints/user_async.py
from fastapi import APIRouter, Query, status
from typing import Optional

from app.api.v1.dependencies import UserServiceDep
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse,
    UserListResponse, UserDetailResponse, UserDeleteResponse
)

router = APIRouter()


@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, user_service: UserServiceDep):  # type: ignore
    user = await user_service.create_user_with_validation(user_data)
    return UserResponse.model_validate(user)


@router.get("/users/", response_model=UserListResponse)
async def get_users(
    user_service: UserServiceDep,  # type: ignore
    skip: int = Query(0),
    limit: int = Query(100, le=1000),
    search: Optional[str] = Query(None)
):
    users, total = await user_service.get_users_with_pagination(skip, limit, search)
    return UserListResponse(
        users=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=(skip // limit) + 1 if limit else 1,
        per_page=limit
    )


@router.get("/users/{user_id}", response_model=UserDetailResponse)
async def get_user(user_id: int, user_service: UserServiceDep):  # type: ignore
    user = await user_service.get_user_with_validation(user_id)
    return UserDetailResponse.model_validate(user)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, user_service: UserServiceDep):  # type: ignore
    updated = await user_service.update_user_with_validation(user_id, user_data)
    return UserResponse.model_validate(updated)


@router.delete("/users/{user_id}", response_model=UserDeleteResponse)
async def delete_user(user_id: int, user_service: UserServiceDep):  # type: ignore
    await user_service.delete_user_with_validation(user_id)
    return UserDeleteResponse(message="User deleted successfully", deleted_user_id=user_id)
