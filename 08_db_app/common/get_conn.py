from dotenv import load_dotenv
import os

from urllib.parse import quote
from sqlalchemy import create_engine

import redis
from elasticsearch import Elasticsearch

load_dotenv()


# SQLite
def get_sqlite_engine(db_url: str = "sqlite:///db.sqlite3"):
    return create_engine(db_url, connect_args={"check_same_thread": False}, pool_size=5, max_overflow=10)


# MariaDB
def get_mariadb_engine():
    user = os.getenv("MARIADB_USER", None)
    password = quote(os.getenv("MARIADB_PASSWORD", None))
    host = os.getenv("MARIADB_HOST", "localhost")
    port = os.getenv("MARIADB_PORT", 3307)
    database = os.getenv("MARIADB_DATABASE", None)

    db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(db_url)


# Redis
def get_redis_client(host="localhost", port=6379, db=0):
    pool = redis.ConnectionPool(host=host, port=port, db=db)
    return redis.StrictRedis(connection_pool=pool)


# Elasticsearch
def get_elasticsearch_client(host="https://localhost:9200", maxsize=10):
    return Elasticsearch(
        hosts=[host],
        maxsize=maxsize
    )
