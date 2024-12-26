import uvicorn
from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Union

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


# create new item
@app.post("/item")
async def creat_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return {"data": item_dict}


# update origin item
@app.put("/item/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


# multi item body data
@app.put("/item/user/{item_id}")
async def update_item_with_user(item_id: int, item: Item, user: User, importance: int = Body()):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# app run as debug
if __name__ == "__main__":
    uvicorn.run("post_item_api:app", port=8001, reload=True)
