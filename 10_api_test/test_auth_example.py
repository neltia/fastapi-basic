import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from get_app import get_app

app = get_app(directory="09_auth", filename="basic_auth_example.py")


async def startup_and_shutdown(app: FastAPI):
    """Manually handle FastAPI app lifespan."""
    await app.router.startup()
    await app.router.shutdown()


@pytest.mark.asyncio
async def test_check_user_who_get():
    await startup_and_shutdown(app)  # Start lifespan manually
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/who")
        assert response.status_code == 200
