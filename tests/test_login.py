from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_login_get():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get('/login')
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to login page!"}



@pytest.fixture
def mock_dependencies(mocker):
    # Мокаем функции, которые вызываются в API
    mock_select_user = mocker.patch('database.actions.with_user.select_user', new_callable=AsyncMock)
    mock_login = mocker.patch('database.actions.with_user.login', new_callable=AsyncMock)
    mock_get_role_by_login = mocker.patch('database.actions.with_user.get_role_by_login', new_callable=AsyncMock)
    mock_add_token = mocker.patch('database.actions.with_token.add_token', new_callable=AsyncMock)

    # Возвращаем моки для настройки в тестах
    return {
        "select_user": mock_select_user,
        "login": mock_login,
        "get_role_by_login": mock_get_role_by_login,
        "add_token": mock_add_token,
    }

@pytest.mark.asyncio
async def test_login_success(mock_dependencies):
    mock_dependencies["select_user"].return_value = True
    mock_dependencies["login"].return_value = True
    mock_dependencies["get_role_by_login"].return_value = "admin"
    mock_dependencies["add_token"].return_value = None
    async with AsyncClient(app=app, base_url="http://test") as client:

        response = await client.post("/login", json={"login": "lia", "password": "lia"})
        assert response.status_code == 200
        assert response.json()["message"] == "success"

@pytest.mark.asyncio
async def test_login_incorrect_password(mock_dependencies):
    mock_dependencies["select_user"].return_value = True
    mock_dependencies["login"].return_value = False
    async with AsyncClient(app=app, base_url="http://test") as client:

        response = await client.post("/login", json={"login": "lia", "password": "wrong_password"})
        assert response.status_code == 200
        assert response.json()["message"] == "Password is incorrect"

@pytest.mark.asyncio
async def test_login_user_not_found(mock_dependencies):
    mock_dependencies["select_user"].return_value = False
    async with AsyncClient(app=app, base_url="http://test") as client:

        response = await client.post("/login", json={"login": "unknown_user", "password": "any_password"})
        assert response.status_code == 200
        assert response.json()["message"] == "There's no user with login 'unknown_user'. Try a different one"

@pytest.mark.asyncio
async def test_login_internal_error(mock_dependencies, mocker):
    mocker.patch("src.routes.login.select_user", side_effect=Exception("Database connection error"))
    mock_dependencies["select_user"].side_effect = Exception("Database connection error")
    async with AsyncClient(app=app, base_url="http://test") as client:

        response = await client.post("/login", json={"login": "lia", "password": "lia"})
        assert response.status_code == 200
        assert response.json()["message"].startswith("An error ")
