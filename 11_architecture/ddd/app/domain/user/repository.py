from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.user.models import User


class SyncUserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_users(self, skip: int = 0, limit: int = 100, search: str = None) -> Tuple[List[User], int]:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass


class AsyncUserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_users(self, skip: int = 0, limit: int = 100, search: str = None) -> Tuple[List[User], int]:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        pass
