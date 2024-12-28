from fastapi import HTTPException
from app_mariadb.repository import MariaDBRepository
from app_mariadb.schemas import ItemCreate, ItemUpdate, ItemResponse
from common.result_helper import create_response


class MariaDBService:
    def __init__(self):
        self.repo = MariaDBRepository()

    def get_all_items(self):
        items = self.repo.get_all()
        data = [ItemResponse.model_validate(item) for item in items]
        return create_response(result_code=200, data=data)

    def create_item(self, item: ItemCreate):
        item_data = item.model_dump()
        new_item = self.repo.create(item_data)
        item_id = new_item.id
        return create_response(result_code=201, data=item_id)

    def get_item_by_id(self, item_id: int):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        data = ItemResponse.model_validate(item)
        return create_response(result_code=200, data=data)

    def update_item(self, item_id: int, item: ItemUpdate):
        item_data = item.model_dump(exclude_unset=True)  # Only include provided fields
        updated_item = self.repo.update(item_id, item_data)
        if not updated_item:
            raise HTTPException(status_code=404, detail="Item not found")

        item_id = updated_item.id
        return create_response(result_code=200, data=item_id)

    def delete_item(self, item_id: int):
        success = self.repo.delete(item_id)
        if not success:
            raise HTTPException(status_code=404, detail="Item not found")

        data = {"message": "Item deleted successfully"}
        return create_response(result_code=200, data=data)
