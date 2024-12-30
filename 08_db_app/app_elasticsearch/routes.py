from fastapi import APIRouter, Depends
from app_elasticsearch.service import get_es_client
from app_elasticsearch.service import get_es_service
from app_elasticsearch.models import ProductCreate, ProductUpdate, ProductSearchQuery
from typing import Optional

es_router = APIRouter()
service = get_es_service()


# Close Elasticsearch on application shutdown
@es_router.on_event("shutdown")
async def shutdown_event():
    await get_es_client().close()


@es_router.get("/products")
async def get_all_products():
    return await service.get_all_products()


@es_router.post("/products")
async def add_products(product: ProductCreate, doc_id: Optional[str] = None):
    result = await service.create_product(doc_id, product)
    return result


@es_router.get("/products/{doc_id}")
async def get_product(doc_id: str):
    result = await service.get_product_by_id(doc_id)
    return result


@es_router.post("/search")
async def search_documents(query: ProductSearchQuery):
    result = await service.search(query)
    return result


@es_router.put("/products/{doc_id}")
async def update_product(doc_id: str, product: ProductUpdate):
    result = await service.update_product(doc_id, product)
    return result


@es_router.delete("/products/{doc_id}")
async def delete_product(doc_id: str):
    result = await service.delete_product(doc_id)
    return result
