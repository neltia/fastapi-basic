# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 동기 및 비동기 세션 설정
if settings.async_mode:
    # 비동기 모드일 때 비동기 엔진과 세션 사용
    SQLALCHEMY_DATABASE_URL = settings.database_async_url
    print(f"Using async database URL: {SQLALCHEMY_DATABASE_URL}")
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,  # SQL 쿼리 로깅
    )
    db_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
else:
    # 동기 모드일 때 동기 엔진과 세션 사용
    SQLALCHEMY_DATABASE_URL = settings.database_url
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,
    )
    db_session = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )
