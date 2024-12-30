from elasticsearch import AsyncElasticsearch


class ElasticsearchRepository:
    def __init__(self, es_client: AsyncElasticsearch, index_name: str):
        self.es_client = es_client
        self.index_name = index_name

    # Create or update a document in Elasticsearch
    async def create_document(self, doc_id: str, document: dict):
        if doc_id:
            response = await self.es_client.index(index=self.index_name, id=doc_id, body=document)
        else:
            response = await self.es_client.index(index=self.index_name, body=document)
        return response

    # Retrieve a document by its ID
    async def get_document(self, doc_id: str):
        response = await self.es_client.get(index=self.index_name, id=doc_id)
        if response.get("found"):
            return response["_source"]
        return None

    # Search for documents using Query DSL
    async def search_documents(self, query: dict):
        response = await self.es_client.search(index=self.index_name, query=query)
        return response

    # Update
    async def update_document(self, doc_id: str, query: dict):
        response = await self.es_client.update(index=self.index_name, id=doc_id, body=query)
        return response

    # Delete a document by its ID
    async def delete_document(self, doc_id: str):
        response = await self.es_client.delete(index=self.index_name, id=doc_id)
        return response
