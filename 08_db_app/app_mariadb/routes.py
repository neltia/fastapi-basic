from fastapi import APIRouter
from app_mariadb.service import MariaDBService
from app_mariadb.schemas import ItemCreate, ItemUpdate

mariadb_router = APIRouter()
service = MariaDBService()


@mariadb_router.get("/items")
def get_items():
    return service.get_all_items()


@mariadb_router.post("/items")
def create_item(item: ItemCreate):
    return service.create_item(item)


@mariadb_router.get("/items/{item_id}")
def get_item(item_id: int):
    return service.get_item_by_id(item_id)


@mariadb_router.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate):
    return service.update_item(item_id, item)


@mariadb_router.delete("/items/{item_id}")
def delete_item(item_id: int):
    return service.delete_item(item_id)
