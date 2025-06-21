import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app_mariadb.models import Base


# 환경변수 기반 설정: MariaDB
DB_USER = os.getenv("MARIADB_USER", "root")
DB_PASSWORD = os.getenv("MARIADB_PASSWORD", "password")
DB_HOST = os.getenv("MARIADB_HOST", "localhost")
DB_PORT = os.getenv("MARIADB_PORT", "3306")
DB_NAME = os.getenv("MARIADB_DATABASE", "test_db")
DATABASE_URL = f"mysql+asyncmy://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy 엔진 및 세션 팩토리 (전역적으로 관리)
engine = create_async_engine(DATABASE_URL, pool_size=5, max_overflow=10, echo=True)
SessionMaker = async_sessionmaker(bind=engine, expire_on_commit=False)


# DB init
# - Initialize the database (e.g., create tables)
async def initialize_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    print(f"Database initialized successfully at {DB_HOST}:{DB_PORT}/{DB_NAME}")


async def provide_session():
    """
    Provide a database session for FastAPI dependency injection.
    """
    async with SessionMaker() as session:
        yield session
