from app.application.user.dto import UserCreateDTO, UserUpdateDTO
from app.domain.user.repository import SyncUserRepository, AsyncUserRepository
from app.domain.user.models import User
from app.core.security import PasswordManager


class SyncUserService:
    def __init__(self, repo: SyncUserRepository):
        self.repo = repo

    def get_user(self, user_id: int) -> User:
        return self.repo.get_user_by_id(user_id)

    def get_users(self, skip: int = 0, limit: int = 100, search: str = None):
        return self.repo.get_users(skip, limit, search)

    def create_user(self, data: UserCreateDTO) -> User:
        hashed = PasswordManager.hash_password(data.password)
        user = User(username=data.username, email=data.email, password_hash=hashed, full_name=data.full_name, is_active=data.is_active)
        return self.repo.create_user(user)

    def update_user(self, user_id: int, data: UserUpdateDTO) -> User:
        user = self.repo.get_user_by_id(user_id)
        for field, value in data.dict(exclude_unset=True).items():
            if field == "password":
                setattr(user, "password_hash", PasswordManager.hash_password(value))
            else:
                setattr(user, field, value)
        return self.repo.update_user(user)

    def delete_user(self, user_id: int) -> bool:
        return self.repo.delete_user(user_id)


class AsyncUserService:
    def __init__(self, repo: AsyncUserRepository):
        self.repo = repo

    async def get_user(self, user_id: int) -> User:
        return await self.repo.get_user_by_id(user_id)

    async def get_users(self, skip: int = 0, limit: int = 100, search: str = None):
        return await self.repo.get_users(skip, limit, search)

    async def create_user(self, data: UserCreateDTO) -> User:
        hashed = PasswordManager.hash_password(data.password)
        user = User(username=data.username, email=data.email, password_hash=hashed, full_name=data.full_name, is_active=data.is_active)
        return await self.repo.create_user(user)

    async def update_user(self, user_id: int, data: UserUpdateDTO) -> User:
        user = await self.repo.get_user_by_id(user_id)
        for field, value in data.dict(exclude_unset=True).items():
            if field == "password":
                setattr(user, "password_hash", PasswordManager.hash_password(value))
            else:
                setattr(user, field, value)
        return await self.repo.update_user(user)

    async def delete_user(self, user_id: int) -> bool:
        return await self.repo.delete_user(user_id)
