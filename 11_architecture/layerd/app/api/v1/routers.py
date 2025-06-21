# app/api/v1/router.py
from fastapi import APIRouter
from app.core.config import settings

from app.api.v1.endpoints import user_sync, user_async

api_router = APIRouter()

if settings.async_mode:
    print("[Router] Using ASYNC router")
    api_router.include_router(user_async.router, prefix="", tags=["users (async)"])
else:
    print("[Router] Using SYNC router")
    api_router.include_router(user_sync.router, prefix="", tags=["users (sync)"])
