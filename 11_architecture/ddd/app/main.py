from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.presentation.api.v1.routers import api_router
from app.config.settings import settings
from app.infrastructure.db.session import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("Starting up FastAPI application...")

    # Create database tables
    try:
        create_tables()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")

    yield

    # Shutdown
    print("Shutting down FastAPI application...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api/v1")
