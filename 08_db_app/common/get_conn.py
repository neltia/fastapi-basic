# env
from dotenv import load_dotenv
import os
from urllib.parse import quote
# RDB
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
# NoSQL
import redis
from elasticsearch import AsyncElasticsearch

load_dotenv()


# SQLite
def get_sqlite_engine(db_url: str = "sqlite:///db.sqlite3"):
    return create_engine(db_url, connect_args={"check_same_thread": False}, pool_size=5, max_overflow=10)


# MariaDB
def get_mariadb_engine_sync():
    user = os.getenv("MARIADB_USER", None)
    password = quote(os.getenv("MARIADB_PASSWORD", None))
    host = os.getenv("MARIADB_HOST", "localhost")
    port = os.getenv("MARIADB_PORT", 3307)
    database = os.getenv("MARIADB_DATABASE", None)

    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(db_url)


def get_mariadb_engine_async():
    user = os.getenv("MARIADB_USER", None)
    password = quote(os.getenv("MARIADB_PASSWORD", None))
    host = os.getenv("MARIADB_HOST", "localhost")
    port = os.getenv("MARIADB_PORT", 3307)
    database = os.getenv("MARIADB_DATABASE", None)

    db_url = f"mysql+asyncmy://{user}:{password}@{host}:{port}/{database}"
    return create_async_engine(db_url)


# Redis
def get_redis_client(host="localhost", port=6379, db=0):
    pool = redis.ConnectionPool(host=host, port=port, db=db)
    return redis.StrictRedis(connection_pool=pool)


# Elasticsearch
def get_elasticsearch_client():
    es_host = os.getenv("ELASTICSEARCH_HOST", "localhost")
    es_port = os.getenv("ELASTICSEARCH_PORT", 9200)
    is_secure = os.getenv("ELASTICSEARCH_SECURE", "True").lower() == "true"

    es_user = os.getenv("ELASTICSEARCH_USER", None)
    es_password = os.getenv("ELASTICSEARCH_PASSWORD", None)
    max_connection = int(os.getenv("ELASTICSEARCH_MAX_CONNECTIONS", 10))

    if not es_host.startswith("http"):
        host_list = get_host_list(es_host, es_port, is_secure=is_secure)
    else:
        host_list = es_host

    es_client = AsyncElasticsearch(
        hosts=host_list,
        basic_auth=(es_user, es_password) if es_user and es_password else None,  # Basic Authentication
        verify_certs=False,  # SSL/TLS 인증 무시 설정, Production에서는 사용 권장
        ssl_show_warn=False,
        # connections_per_node=max_connection
    )
    return es_client


def get_host_list(host_data, es_port, is_secure=True):
    protocol = "https" if is_secure else "http"

    host_list = list()
    if "," not in host_data:
        host_data = f"{protocol}://{host_data}:{es_port}"
        host_list.append(host_data)
        return host_list

    for host in host_data.split(","):
        host_data = f"{protocol}://{host}:{es_port}"
        host_list.append(host_data)
    return host_list


async def test_elasticsearch_connection():
    es_client = get_elasticsearch_client()
    try:
        if await es_client.ping():
            print("Elasticsearch connection successful.")
        else:
            print("Elasticsearch connection failed.")
    finally:
        await es_client.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_elasticsearch_connection())
