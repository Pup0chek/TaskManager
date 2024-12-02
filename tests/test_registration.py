# import pytest
# from unittest.mock import AsyncMock, patch
# from fastapi.testclient import TestClient
# from httpx import AsyncClient
# from src.main import app
# from database.models import User
# from src.models import User_py
#
#
# client = TestClient(app)
#
# # Мокируем функции для тестирования
# @pytest.fixture
# def mock_dependencies(mocker):
#     # Мокаем функции, которые вызываются в API
#     mock_select_user = mocker.patch('database.actions.with_user.select_user', new_callable=AsyncMock)
#     mock_create_user = mocker.patch('database.actions.with_user.create_user', new_callable=AsyncMock)
#     mock_add_token = mocker.patch('database.actions.with_token.add_token', new_callable=AsyncMock)
#     mock_redis_set = mocker.patch('aioredis.StrictRedis.set', new_callable=AsyncMock)
#     mock_redis_get = mocker.patch('aioredis.StrictRedis.get', return_value=b"mock_token")
#
#     return {
#         "select_user": mock_select_user,
#         "create_user": mock_create_user,
#         "add_token": mock_add_token,
#         "redis_set": mock_redis_set,
#         "redis_get": mock_redis_get,
#     }
#
# # Тест для страницы регистрации
# @pytest.mark.asyncio
# async def test_get_registration():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/registration/")
#         assert response.status_code == 200
#         assert response.json() == {"message": "Welcome to registration page!"}
#
# # Тест на успешную регистрацию пользователя
# @pytest.mark.asyncio
# async def test_post_registration_success(mock_dependencies):
#     user_data = {
#         "login": "new_user",
#         "password": "password123",
#         "role": "user"
#     }
#
#     # Мокаем зависимости
#     mock_dependencies["select_user"].return_value = None  # Пользователь не найден
#     mock_dependencies["create_user"].return_value = "User with ID 1 was successfully created."  # Успешное создание
#     mock_dependencies["add_token"].return_value = None  # Токен добавлен успешно
#     mock_dependencies["redis_set"].return_value = None  # Успешная запись в Redis
#
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.post("/registration/", json=user_data)
#
#         # Проверка правильности статуса и данных в ответе
#         assert response.status_code == 200
#         assert response.json()["message"] == "User with ID 1 was successfully created."
#         assert "access_token" in response.json()
#         assert "refresh_token" in response.json()
#
#         # Проверка вызова Redis для записи токенов
#         assert mock_dependencies["redis_set"].call_count == 2  # Должно быть два вызова для записи access и refresh токенов
#
# # Тест на уже существующего пользователя
# @pytest.mark.asyncio
# async def test_post_registration_user_exists(mock_dependencies):
#     user_data = {
#         "login": "existing_user",
#         "password": "password123",
#         "role": "user"
#     }
#
#     # Мокаем зависимость select_user, чтобы вернуть существующего пользователя
#     mock_dependencies["select_user"].return_value = User(login="existing_user", password="password123", role="user")
#
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.post("/registration/", json=user_data)
#
#         # Проверка ответа на уже существующего пользователя
#         assert response.status_code == 200
#         assert response.json() == {"message": "User with login 'existing_user' already exists."}
#
# # Тест на ошибку при создании пользователя
# @pytest.mark.asyncio
# async def test_post_registration_error(mock_dependencies):
#     user_data = {
#         "login": "new_user_error",
#         "password": "password123",
#         "role": "user"
#     }
#
#     # Мокаем ошибку при создании пользователя
#     mock_dependencies["select_user"].return_value = None  # Пользователь не найден
#     mock_dependencies["create_user"].side_effect = Exception("Database connection error")
#
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.post("/registration/", json=user_data)
#
#         # Проверка ошибки в процессе регистрации
#         assert response.status_code == 200
#         assert response.json()["message"].startswith("An error ")
#
# # Тест на успешную регистрацию и добавление токенов в Redis
# @pytest.mark.asyncio
# async def test_post_registration_tokens(mock_dependencies):
#     user_data = {
#         "login": "user_for_tokens",
#         "password": "password123",
#         "role": "user"
#     }
#
#     # Мокаем успешную регистрацию
#     mock_dependencies["select_user"].return_value = None  # Пользователь не найден
#     mock_dependencies["create_user"].return_value = "User with ID 1 was successfully created."  # Успешное создание
#     mock_dependencies["add_token"].return_value = None  # Токен добавлен успешно
#     mock_dependencies["redis_set"].return_value = None  # Успешная запись в Redis
#
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.post("/registration/", json=user_data)
#
#         # Проверка правильности статуса и данных в ответе
#         assert response.status_code == 200
#         assert response.json()["message"] == "User with ID 1 was successfully created."
#         assert "access_token" in response.json()
#         assert "refresh_token" in response.json()
#
#         # Проверка, что Redis был вызван дважды
#         assert mock_dependencies["redis_set"].call_count == 2  # Два вызова для записи токенов
