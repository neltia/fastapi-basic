from dotenv import load_dotenv
import os
from fastapi import HTTPException
from common.get_conn import get_elasticsearch_client
from app_elasticsearch.repository import ElasticsearchRepository
from app_elasticsearch.models import ProductResponse, ProductCreate, ProductUpdate, ProductSearchQuery
from common.result_helper import create_response

load_dotenv()


def get_es_client():
    es_client = get_elasticsearch_client()
    return es_client


def get_es_service():
    es_client = get_es_client()
    products_index = os.getenv("PRODUCTS_INDEX", "products")
    repository = ElasticsearchRepository(es_client, products_index)
    return ElasticsearchService(repository)


class ElasticsearchService:
    def __init__(self, repository: ElasticsearchRepository):
        self.repo = repository

    async def get_all_products(self):
        query = {"match_all": {}}
        product_list = await self.repo.search_documents(query)
        data = [ProductResponse.model_validate(product) for product in product_list]
        return create_response(result_code=200, data=data)

    async def create_product(self, doc_id: str, product: ProductCreate):
        product_data = product.model_dump()
        response = await self.repo.create_document(doc_id=doc_id, document=product_data)
        if response["result"] != "created":
            raise HTTPException(status_code=500, detail="Failed to create product")
        return create_response(result_code=201, data="created")

    async def get_product_by_id(self, doc_id: str):
        product = await self.repo.get_document(doc_id=doc_id)
        if product is None:
            return create_response(result_code=404, data="Product not found")
        return create_response(result_code=200, data=product)

    async def update_product(self, doc_id: str, product: ProductUpdate):
        update_data = product.model_dump(exclude_unset=True)
        response = await self.repo.update_document(doc_id, {"doc": update_data})
        if response["result"] != "updated":
            raise HTTPException(status_code=500, detail="Failed to update product")
        return create_response(result_code=200, data="updated")

    async def delete_product(self, doc_id: str):
        response = await self.repo.delete_document(doc_id)
        if response.get("result") != "deleted":
            raise HTTPException(status_code=404, detail="Product not found")
        return create_response(result_code=200, data="Product deleted successfully")

    async def search(self, query: ProductSearchQuery):
        query_dsl = {
            "query": {
                "bool": {
                    "must": [{"match": {"name": query.query}}] if query.query else []
                }
            }
        }

        response = await self.repo.search_documents(query=query_dsl["query"])
        total = response["hits"]["total"]["value"]
        product_list = [hit["_source"] for hit in response["hits"]["hits"]]
        data = {"total": total, "list": product_list}
        return create_response(result_code=200, data=data)
