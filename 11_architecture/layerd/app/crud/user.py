""" /app/crud/user.py """
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import PasswordManager


class UserCRUD:
    """User CRUD operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> tuple[List[User], int]:
        """Get users with pagination and optional search"""
        query = self.db.query(User)

        if search:
            search_filter = or_(
                User.username.contains(search),
                User.email.contains(search),
                User.full_name.contains(search)
            )
            query = query.filter(search_filter)

        total = query.count()
        users = query.offset(skip).limit(limit).all()

        return users, total

    def create_user(self, user_data: UserCreate) -> User:
        """Create new user"""
        # Hash password
        hashed_password = PasswordManager.hash_password(user_data.password)

        # Create user instance
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            full_name=user_data.full_name,
            is_active=user_data.is_active
        )

        # Add to database
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        # Handle password hashing if password is being updated
        if "password" in update_data:
            update_data["password_hash"] = PasswordManager.hash_password(update_data.pop("password"))

        # Update user attributes
        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()

        return True

    def check_username_exists(self, username: str, exclude_user_id: Optional[int] = None) -> bool:
        """Check if username exists"""
        query = self.db.query(User).filter(User.username == username)
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        return query.first() is not None

    def check_email_exists(self, email: str, exclude_user_id: Optional[int] = None) -> bool:
        """Check if email exists"""
        query = self.db.query(User).filter(User.email == email)
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        return query.first() is not None
