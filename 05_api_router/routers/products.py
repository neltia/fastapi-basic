from fastapi import APIRouter

product_router = APIRouter(prefix="/products", tags=["products"])


@product_router.get("/")
def get_products():
    return [{"id": 101, "name": "Laptop"}, {"id": 102, "name": "Smartphone"}]


@product_router.post("/")
def add_product(name: str):
    return {"message": f"Product {name} added"}
