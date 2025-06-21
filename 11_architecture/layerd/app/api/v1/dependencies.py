from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.base import get_db
from app.db.session import get_async_db
from app.crud.user import UserCRUD
from app.crud.user_async import AsyncUserCRUD
from app.services.user import UserService
from app.core.config import settings


# Async mode DI
async def get_async_user_crud(db: AsyncSession = Depends(get_async_db)) -> AsyncUserCRUD:
    return AsyncUserCRUD(db)


async def get_async_user_service(
    crud: AsyncUserCRUD = Depends(get_async_user_crud)
) -> UserService:
    return UserService(crud)


# Sync mode DI
def get_sync_user_crud(db: Session = Depends(get_db)) -> UserCRUD:
    return UserCRUD(db)


def get_sync_user_service(
    crud: UserCRUD = Depends(get_sync_user_crud)
) -> UserService:
    return UserService(crud)


# Final binding
if settings.async_mode:
    UserServiceDep = Annotated[UserService, Depends(get_async_user_service)]
    UserCRUDDep = Annotated[AsyncUserCRUD, Depends(get_async_user_crud)]
else:
    UserServiceDep = Annotated[UserService, Depends(get_sync_user_service)]
    UserCRUDDep = Annotated[UserCRUD, Depends(get_sync_user_crud)]
