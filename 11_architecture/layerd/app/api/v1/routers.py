from fastapi import APIRouter
from app.api.v1.endpoints import user

# Create main API router
api_router = APIRouter()

# Include user endpoints
api_router.include_router(user.router, tags=["users"])
