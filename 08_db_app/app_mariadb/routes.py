from fastapi import APIRouter
from app_mariadb.service import MariaDBService
from app_mariadb.schemas import ItemCreate, ItemUpdate

mariadb_router = APIRouter()
service = MariaDBService()


@mariadb_router.on_event("startup")
async def startup_event():
    await service.init_db()
    print("Database initialization completed.")


@mariadb_router.get("/items")
async def get_items():
    return await service.get_all_items()


@mariadb_router.post("/items")
async def create_item(item: ItemCreate):
    return await service.create_item(item)


@mariadb_router.get("/items/{item_id}")
async def get_item(item_id: int):
    return await service.get_item_by_id(item_id)


@mariadb_router.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemUpdate):
    return await service.update_item(item_id, item)


@mariadb_router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return await service.delete_item(item_id)
