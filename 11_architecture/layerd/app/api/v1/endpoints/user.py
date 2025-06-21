from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.crud.user import UserCRUD
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse,
    UserListResponse, UserDetailResponse, UserDeleteResponse
)

router = APIRouter()


@router.post("/users/", response_model=UserResponse, status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user"""
    crud = UserCRUD(db)

    # Check if username already exists
    if crud.check_username_exists(user_data.username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Check if email already exists
    if crud.check_email_exists(user_data.email):
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    try:
        user = crud.create_user(user_data)
        return UserResponse.model_validate(user)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create user: {str(e)}"
        )


@router.get("/users/", response_model=UserListResponse)
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all users with pagination and search"""
    crud = UserCRUD(db)
    users, total = crud.get_users(skip=skip, limit=limit, search=search)

    user_responses = [UserResponse.model_validate(user) for user in users]

    return UserListResponse(
        users=user_responses,
        total=total,
        page=(skip // limit) + 1 if limit > 0 else 1,
        per_page=limit
    )


@router.get("/users/{user_id}", response_model=UserDetailResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific user by ID"""
    crud = UserCRUD(db)
    user = crud.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return UserDetailResponse.model_validate(user)


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update a user"""
    crud = UserCRUD(db)

    # Check if user exists
    existing_user = crud.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check for username conflicts
    if user_data.username and crud.check_username_exists(user_data.username, exclude_user_id=user_id):
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Check for email conflicts
    if user_data.email and crud.check_email_exists(user_data.email, exclude_user_id=user_id):
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    try:
        updated_user = crud.update_user(user_id, user_data)
        return UserResponse.model_validate(updated_user)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update user: {str(e)}"
        )


@router.delete("/users/{user_id}", response_model=UserDeleteResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a user"""
    crud = UserCRUD(db)

    # Check if user exists
    existing_user = crud.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    try:
        success = crud.delete_user(user_id)
        if success:
            return UserDeleteResponse(
                message="User deleted successfully",
                deleted_user_id=user_id
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete user"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete user: {str(e)}"
        )
