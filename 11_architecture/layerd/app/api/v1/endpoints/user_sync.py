# app/api/v1/endpoints/user_sync.py
from fastapi import APIRouter, Query, status
from typing import Optional

from app.api.v1.dependencies import UserServiceDep
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse,
    UserListResponse, UserDetailResponse, UserDeleteResponse
)

router = APIRouter()


@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, user_service: UserServiceDep):  # type: ignore
    user = user_service.crud.create_user(user_data)
    return UserResponse.model_validate(user)


@router.get("/users/", response_model=UserListResponse)
def get_users(
    user_service: UserServiceDep,  # type: ignore
    skip: int = Query(0),
    limit: int = Query(100, le=1000),
    search: Optional[str] = Query(None)
):
    users, total = user_service.crud.get_users(skip=skip, limit=limit, search=search)
    return UserListResponse(
        users=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=(skip // limit) + 1 if limit else 1,
        per_page=limit
    )


@router.get("/users/{user_id}", response_model=UserDetailResponse)
def get_user(user_id: int, user_service: UserServiceDep):  # type: ignore
    user = user_service.crud.get_user_by_id(user_id)
    return UserDetailResponse.model_validate(user)


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, user_service: UserServiceDep):  # type: ignore
    updated = user_service.crud.update_user(user_id, user_data)
    return UserResponse.model_validate(updated)


@router.delete("/users/{user_id}", response_model=UserDeleteResponse)
def delete_user(user_id: int, user_service: UserServiceDep):  # type: ignore
    user_service.crud.delete_user(user_id)
    return UserDeleteResponse(message="User deleted successfully", deleted_user_id=user_id)
