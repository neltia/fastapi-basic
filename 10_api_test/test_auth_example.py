import pytest
from httpx import ASGITransport, AsyncClient
from get_app import get_app

app = get_app(directory="09_auth", filename="basic_auth_example.py")


@pytest.mark.asyncio
async def test_check_user_who_get():
    # FastAPI lifespan 처리
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/who")
        assert response.status_code == 401
