from fastapi import APIRouter
from app.config.settings import settings

if settings.ASYNC_MODE:
    from app.presentation.api.v1.endpoints.user_async import router as user_router
else:
    from app.presentation.api.v1.endpoints.user_sync import router as user_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["users"])
