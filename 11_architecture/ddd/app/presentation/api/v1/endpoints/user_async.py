from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import AsyncSessionLocal
from app.infrastructure.persistence.async_user_repository import SqlAsyncUserRepository
from app.application.user.service import AsyncUserService
from app.application.user.dto import UserCreateDTO, UserDTO

router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


def get_service(db: AsyncSession = Depends(get_db)):
    repo = SqlAsyncUserRepository(db)
    return AsyncUserService(repo)


@router.get("/", response_model=List[UserDTO])
async def list_users(service: AsyncUserService = Depends(get_service)):
    return await service.get_users()


@router.post("/", response_model=UserDTO)
async def create_user(user: UserCreateDTO, service: AsyncUserService = Depends(get_service)):
    return await service.create_user(user)


@router.get("/{user_id}", response_model=UserDTO)
async def get_user(user_id: int, service: AsyncUserService = Depends(get_service)):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
