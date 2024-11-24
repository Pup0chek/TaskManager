from fastapi import APIRouter
from src.models import User_py
from database.models import User
from database.connect_to_db import async_session
from database.actions.with_user import create_user, select_user
from src.Token import Token
from database.actions.with_token import add_token

registration_router = APIRouter(prefix='/registration', tags=['Registration'])


@registration_router.get("/")
async def get_registration():
    return {"message": "Welcome to registration page!"}


@registration_router.post("/")
async def post_registration(user: User_py):
    user1 = User(login=user.login, password=user.password, role=user.role)

    async with async_session() as session:
        try:
            user_exists = await select_user(user.login, session)
            if user_exists:
                return {"message": f"User with login '{user.login}' already exists."}
            message = await create_user(user1, session)
            token_access = Token.create_access_token({'login': user.login, 'password': user.password})
            token_refresh = Token.create_refresh_token({"user": user.login, "role": user.role})
            await add_token(user.login, token_access, session)

            return {
                "message": f"{message}",
                "access_token": token_access,
                "refresh_token": token_refresh
            }
        except Exception as e:
            return {"message": f"An error occurred: {e}"}
