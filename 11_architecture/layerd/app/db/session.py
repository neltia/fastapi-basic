from sqlalchemy.orm import Session
from typing import Generator, AsyncGenerator
from app.db.base import SessionLocal
from app.db.base_async import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


def get_db() -> Generator[Session, None, None]:
    """Sync DB 세션"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Async DB 세션"""
    async with AsyncSessionLocal() as session:
        yield session
