from fastapi import APIRouter
from src.models import User_login
from database.connect_to_db import async_session
from database.actions.with_token import add_token
from database.actions.with_user import select_user, login, get_role_by_login
from src.Token import Token

login_router = APIRouter(prefix='/login', tags=['Login'])


@login_router.get("/")
async def get_login():
    return {"message": "Welcome to login page!"}


@login_router.post("/")
async def post_login(user: User_login):
    async with async_session() as session:
        try:
            user_exists = await select_user(user.login, session)
            if user_exists:
                valid_login = await login(user.login, user.password, session)
                if valid_login:
                    role = await get_role_by_login(user.login, session)
                    token_access = Token.create_access_token({"user": user.login, "role": role})
                    token_refresh = Token.create_refresh_token({"user": user.login, "role": role})
                    await add_token(user.login, token_access, session)

                    return {
                        "message": "success",
                        "access_token": token_access,
                        "refresh_token": token_refresh,
                    }
                else:
                    return {"message": "Password is incorrect"}
            else:
                return {"message": f"There's no user with login '{user.login}'. Try a different one"}
        except Exception as e:
            return {"message": f"An error occurred: {e}"}
