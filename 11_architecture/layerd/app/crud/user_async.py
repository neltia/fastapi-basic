"""/app/crud/user_async.py"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from typing import List, Optional, Tuple

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import PasswordManager


class AsyncUserCRUD:
    """Async User CRUD operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by their ID"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by their username"""
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> Tuple[List[User], int]:
        """
        Get a list of users with optional search and pagination.
        Returns the list of users and the total count.
        """
        query = select(User)
        count_query = select(func.count(User.id))

        # Apply search filter if provided
        if search:
            search_filter = or_(
                User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.full_name.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        # Get total count
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Get paginated user list
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        users = result.scalars().all()

        return list(users), total

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        hashed_password = PasswordManager.hash_password(user_data.password)

        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            full_name=user_data.full_name,
            is_active=user_data.is_active
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update an existing user"""
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password_hash"] = PasswordManager.hash_password(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(db_user, field, value)

        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID"""
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return False

        await self.db.delete(db_user)
        await self.db.commit()
        return True

    async def check_username_exists(
        self,
        username: str,
        exclude_user_id: Optional[int] = None
    ) -> bool:
        """Check if the username already exists, excluding a specific user ID if provided"""
        query = select(User.id).where(User.username == username)
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)

        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def check_email_exists(
        self,
        email: str,
        exclude_user_id: Optional[int] = None
    ) -> bool:
        """Check if the email already exists, excluding a specific user ID if provided"""
        query = select(User.id).where(User.email == email)
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)

        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_user_count(self) -> int:
        """Get total number of users"""
        result = await self.db.execute(select(func.count(User.id)))
        return result.scalar()
