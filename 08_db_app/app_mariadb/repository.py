from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import update, delete

from common.get_conn import get_mariadb_engine_async
from app_mariadb.models import Base, Item

engine = get_mariadb_engine_async()


class MariaDBRepository:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = async_sessionmaker(bind=self.engine, expire_on_commit=False)
        self.initialize_database()  # In Production, not recommend. change it: @router.on_event("startup")

    async def initialize_database(self):
        """
        Initialize the database by creating tables if they do not exist.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Tables created successfully.")

    async def get_all(self):
        async with self.SessionLocal() as session:
            result = await session.execute(select(Item))
            return result.scalars().all()

    async def create(self, item: dict):
        async with self.SessionLocal() as session:
            new_item = Item(**item)
            session.add(new_item)
            await session.commit()
            await session.refresh(new_item)
            return new_item

    async def get_by_id(self, item_id: int):
        async with self.SessionLocal() as session:
            result = await session.execute(select(Item).where(Item.id == item_id))
            return result.scalar_one_or_none()

    async def update(self, item_id: int, updates: dict):
        async with self.SessionLocal() as session:
            stmt = (
                update(Item)
                .where(Item.id == item_id)
                .values(**updates)
                .execution_options(synchronize_session="fetch")
            )
            _ = await session.execute(stmt)
            await session.commit()
            # Return the updated item
            return await self.get_by_id(item_id)

    async def delete(self, item_id: int):
        async with self.SessionLocal() as session:
            stmt = delete(Item).where(Item.id == item_id)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0
