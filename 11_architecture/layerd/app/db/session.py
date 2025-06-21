from sqlalchemy.orm import Session
from typing import AsyncGenerator, Generator
from contextlib import contextmanager, asynccontextmanager
from app.db.base import SessionLocal


class DatabaseSession:
    """Database session manager for both sync and async operations"""

    @staticmethod
    def get_sync_session() -> Generator[Session, None, None]:
        """Get synchronous database session"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    @contextmanager
    def get_sync_session_context():
        """Context manager for synchronous database session"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    async def get_async_session() -> AsyncGenerator[Session, None]:
        """Async database session (simulated)"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    @asynccontextmanager
    async def get_async_session_context():
        """Async context manager for database session"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


# Database dependency functions
def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[Session, None]:
    """FastAPI dependency for async database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
