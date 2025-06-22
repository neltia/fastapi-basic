from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

Base = declarative_base()

# 비동기 및 동기 세션 설정을 동적으로 전환
if settings.ASYNC_MODE:
    # 비동기 모드에서는 aiomysql을 사용하도록 설정
    async_database_url = settings.DATABASE_URL.replace("mysql+pymysql://", "mysql+aiomysql://")
    engine = create_async_engine(async_database_url, **settings.database_config)
    AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
else:
    # 동기 모드에서는 pymysql을 사용
    engine = create_engine(settings.DATABASE_URL, **settings.database_config)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Create tables (using session.run_sync to call sync method in an async context)
async def create_tables():
    async with AsyncSessionLocal() as session:
        # Create tables in the database
        async with session.begin():
            # Run sync method for creating tables (since Base.metadata.create_all is sync)
            session.run_sync(Base.metadata.create_all)
