# app/services/user.py
from fastapi import HTTPException, status
from typing import Union

from app.crud.user import UserCRUD
from app.crud.user_async import AsyncUserCRUD
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, crud: Union[UserCRUD, AsyncUserCRUD]):
        self.crud = crud
        self.is_async = isinstance(crud, AsyncUserCRUD)

    async def create_user_with_validation(self, user_data: UserCreate):
        if self.is_async:
            username_exists = await self.crud.check_username_exists(user_data.username)
            email_exists = await self.crud.check_email_exists(user_data.email)
        else:
            username_exists = self.crud.check_username_exists(user_data.username)
            email_exists = self.crud.check_email_exists(user_data.email)

        if username_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        if email_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        return await self.crud.create_user(user_data) if self.is_async else self.crud.create_user(user_data)

    async def update_user_with_validation(self, user_id: int, user_data: UserUpdate):
        existing_user = await self.crud.get_user_by_id(user_id) if self.is_async else self.crud.get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user_data.username:
            exists = await self.crud.check_username_exists(user_data.username, exclude_user_id=user_id) if self.is_async else self.crud.check_username_exists(user_data.username, exclude_user_id=user_id)
            if exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

        if user_data.email:
            exists = await self.crud.check_email_exists(user_data.email, exclude_user_id=user_id) if self.is_async else self.crud.check_email_exists(user_data.email, exclude_user_id=user_id)
            if exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        return await self.crud.update_user(user_id, user_data) if self.is_async else self.crud.update_user(user_id, user_data)

    async def delete_user_with_validation(self, user_id: int):
        user = await self.crud.get_user_by_id(user_id) if self.is_async else self.crud.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        success = await self.crud.delete_user(user_id) if self.is_async else self.crud.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete user")

        return True

    async def get_user_with_validation(self, user_id: int):
        user = await self.crud.get_user_by_id(user_id) if self.is_async else self.crud.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_users_with_pagination(self, skip: int = 0, limit: int = 100, search: str = None):
        return await self.crud.get_users(skip=skip, limit=limit, search=search) if self.is_async else self.crud.get_users(skip=skip, limit=limit, search=search)
