import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app  # Импортируйте приложение FastAPI из основного файла
from src.models import User_login

client = TestClient(app)

# Создаем фиктивные данные
mock_user = User_login(login="lia", password="lia")
mock_role = "admin"
mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoibGlhIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzMxOTM5ODg1fQ.UX9DsE25X2LjxHciTBsV--5rIDYLTMraedDrDIt0ugk"

# Патчим зависимости
@pytest.fixture
def mock_session():
    with patch("database.connect_to_db.Session") as mock_session:
        yield mock_session

@pytest.fixture
def mock_select_user():
    with patch("database.actions.with_user.select_user") as mock_select_user:
        yield mock_select_user

@pytest.fixture
def mock_login():
    with patch("database.actions.with_user.login") as mock_login:
        yield mock_login

@pytest.fixture
def mock_get_role_by_login():
    with patch("database.actions.with_user.get_role_by_login") as mock_get_role_by_login:
        yield mock_get_role_by_login

@pytest.fixture
def mock_token_creation():
    with patch("src.Token.Token.create_token") as mock_create_token:
        mock_create_token.return_value = mock_token
        yield mock_create_token

# Тестируем успешный логин
def test_post_login_success(mock_session, mock_select_user, mock_login, mock_get_role_by_login, mock_token_creation):
    # Настраиваем фиктивные зависимости
    mock_select_user.return_value = True
    mock_login.return_value = True
    mock_get_role_by_login.return_value = mock_role

    response = client.post(
        "/login/",
        json={"login": mock_user.login, "password": mock_user.password},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "success", "token": mock_token}

# Тестируем неверный пароль
def test_post_login_incorrect_password(mock_session, mock_select_user, mock_login, mock_get_role_by_login):
    mock_select_user.return_value = True
    mock_login.return_value = False

    response = client.post(
        "/login/",
        json={"login": mock_user.login, "password": "wrong_password"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Password is incorrect"}

# Тестируем, если пользователь не найден
def test_post_login_user_not_found(mock_session, mock_select_user, mock_login, mock_get_role_by_login):
    mock_select_user.return_value = False

    response = client.post(
        "/login/",
        json={"login": "nonexistent_user", "password": "any_password"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "There's no user with login 'nonexistent_user'. Try different one"}

# Тестируем обработку исключений
def test_post_login_exception(mock_session, mock_select_user, mock_login, mock_get_role_by_login):
    mock_select_user.side_effect = Exception("Database error")

    response = client.post(
        "/login/",
        json={"login": mock_user.login, "password": mock_user.password},
    )

    assert response.status_code == 200
    assert response.json()["message"].startswith("error: Database error")
