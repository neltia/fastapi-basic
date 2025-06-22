# app/controllers/user_controller.py
# 사용자 CRUD 요청을 처리하는 컨트롤러
from fastapi import APIRouter, HTTPException, Query
from app.services.user_service import (
    create_user,
    get_user_data,
    update_user,
    delete_user,
    get_user_list
)
from app.views.user_view import UserView
from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
)

router = APIRouter()


@router.post("/users/", response_model=dict)
async def create_user_endpoint(user: UserCreate):
    user_obj = await create_user(user)
    return UserView.single(user_obj).model_dump()


@router.get("/users/{user_id}", response_model=dict)
async def get_user_endpoint(user_id: int):
    user_obj = await get_user_data(user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    return UserView.single(user_obj).model_dump()


@router.get("/users/", response_model=dict)
async def list_users_endpoint(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
):
    users, total = await get_user_list(page, per_page)
    return UserView.list(users, total, page, per_page).model_dump()


@router.put("/users/{user_id}", response_model=dict)
async def update_user_endpoint(user_id: int, user: UserUpdate):
    user_obj = await update_user(user_id, user)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    return UserView.single(user_obj).model_dump()


@router.delete("/users/{user_id}", response_model=dict)
async def delete_user_endpoint(user_id: int):
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return UserView.delete(user_id).model_dump()
