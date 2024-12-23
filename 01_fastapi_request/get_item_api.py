from fastapi import FastAPI
import uvicorn

app = FastAPI()

fake_items_db = [{"item_name": "First"}, {"item_name": "Second"}, {"item_name": "Third"}]


# all item
@app.get("/items")
async def get_all_items():
    return {"msg": "get all items"}


# get item
@app.get("/item/{item_id}")
async def get_item(item_id: int):
    return {"msg": f"select item: {item_id}"}


# get item list by query param
@app.get("/item/list")
async def get_item_list(skip: int = 0, limit: int = 10):
    data = fake_items_db[skip: skip + limit]
    return {"data": data}


# app run as debug
if __name__ == "__main__":
    uvicorn.run("get_item_api:app", port=8000, reload=True)
