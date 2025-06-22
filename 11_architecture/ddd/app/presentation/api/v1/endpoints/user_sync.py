from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.infrastructure.db.session import SessionLocal
from app.infrastructure.persistence.sync_user_repository import SqlSyncUserRepository
from app.application.user.service import SyncUserService
from app.application.user.dto import UserCreateDTO, UserDTO

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db: Session = Depends(get_db)):
    repo = SqlSyncUserRepository(db)
    return SyncUserService(repo)


@router.get("/", response_model=List[UserDTO])
def list_users(service: SyncUserService = Depends(get_service)):
    return service.get_users()


@router.post("/", response_model=UserDTO)
def create_user(user: UserCreateDTO, service: SyncUserService = Depends(get_service)):
    return service.create_user(user)


@router.get("/{user_id}", response_model=UserDTO)
def get_user(user_id: int, service: SyncUserService = Depends(get_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
