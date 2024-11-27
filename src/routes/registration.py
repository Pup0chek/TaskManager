import aioredis
from fastapi import APIRouter, Depends
from src.models import User_py
from database.models import User
from database.connect_to_db import async_session
from database.actions.with_user import create_user, select_user
from src.Token import Token
from database.actions.with_token import add_token

registration_router = APIRouter(prefix='/registration', tags=['Registration'])


async def redis_client():
    return await aioredis.StrictRedis(host="localhost", port="6379", db=0)


@registration_router.get("/")
async def get_registration():
    return {"message": "Welcome to registration page!"}


@registration_router.post("/")
async def post_registration(user: User_py, client=Depends(redis_client)):
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
            await client.set(f'access:user:{user.login}', token_access)
            await client.set(f'refresh:user:{user.login}', token_refresh)

            access = await client.get(f'access:user:{user.login}')
            refresh = await client.get(f'refresh:user:{user.login}')

            return {
                "message": f"{message}",
                "access_token": access.decode('utf-8'),
                "refresh_token": refresh.decode('utf-8')
            }
        except Exception as e:
            return {"message": f"An error occurred: {e}"}
