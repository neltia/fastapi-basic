from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import Tuple, List, Optional

from app.domain.user.repository import SyncUserRepository
from app.domain.user.models import User


class SqlSyncUserRepository(SyncUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    def get_users(self, skip: int = 0, limit: int = 100, search: str = None) -> Tuple[List[User], int]:
        query = select(User)
        count_query = select(func.count(User.id))
        if search:
            query = query.where(User.username.ilike(f"%{search}%"))
            count_query = count_query.where(User.username.ilike(f"%{search}%"))
        total = self.db.execute(count_query).scalar()
        users = self.db.execute(query.offset(skip).limit(limit)).scalars().all()
        return users, total

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
