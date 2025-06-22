from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple, List, Optional

from app.domain.user.repository import AsyncUserRepository
from app.domain.user.models import User


class SqlAsyncUserRepository(AsyncUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_users(self, skip: int = 0, limit: int = 100, search: str = None) -> Tuple[List[User], int]:
        query = select(User)
        count_query = select(func.count(User.id))
        if search:
            query = query.where(User.username.ilike(f"%{search}%"))
            count_query = count_query.where(User.username.ilike(f"%{search}%"))
        total = (await self.db.execute(count_query)).scalar()
        users = (await self.db.execute(query.offset(skip).limit(limit))).scalars().all()
        return users, total

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True
