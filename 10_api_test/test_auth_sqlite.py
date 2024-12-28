import pytest
from httpx import AsyncClient
from get_app import get_app

app = get_app(directory="09_auth", filename="basic_auth_sqlite.py")


@pytest.mark.asyncio
async def test_login_with_cookie_login_cookie_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login/cookie")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_with_session_login_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_logged_in_user_me_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/me")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_logout_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/logout")
        assert response.status_code == 200
