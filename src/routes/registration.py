from hashlib import md5

from fastapi.templating import Jinja2Templates

# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.responses import HTMLResponse
#from starlette.templating import Jinja2Templates

import aioredis
from fastapi import APIRouter, Depends, Request, HTTPException


from src.models import User_py
from database.models import User
from database.connect_to_db import async_session
from database.actions.with_user import create_user, select_user
from src.Token import Token
from database.actions.with_token import add_token

registration_router = APIRouter(prefix='/registration', tags=['Registration'])
templates = Jinja2Templates(directory="templates")

async def redis_client():
    return await aioredis.StrictRedis(host="localhost", port="6379", db=0)

async def cache_path(path: str, response_data: str):
    async with async_session() as session:
        r = await redis_client()
        path_hash = md5(path.encode()).hexdigest()
        await r.set(path_hash, response_data, ex=3600)

async def get_cached_path(path: str) -> str:
    async with async_session() as session:
        r = await redis_client()
        path_hash = md5(path.encode()).hexdigest()
        cached_data = await r.get(path_hash)
        return cached_data


@registration_router.get("/")
async def get_registration(request : Request):
    async with async_session() as session:
        cached_data = await get_cached_path('/registration')
        if cached_data:
            json = {"path": '/registration', "cached": True, "data": cached_data}
            html = templates.TemplateResponse('registration.html', {"request": request, **json})
            return html

        response_data = "Welcome to registration page!"

        await cache_path('/registration', response_data)

        json = {"path": '/registration', "cached": False, "data": response_data}
        html = templates.TemplateResponse('registration.html', {"request":request, **json})
        return html


@registration_router.post("/")
async def post_registration(user: User_py, client=Depends(redis_client)):
    user1 = User(login=user.login, password=user.password, role=user.role)

    async with async_session() as session:
        try:
            user_exists = await select_user(user.login, session)
            if user_exists:
                #return {"message": f"User with login '{user.login}' already exists."}
                raise HTTPException(status_code=401, detail=f"User with login '{user.login}' already exists.")
            message = await create_user(user1, session)
            token_access = Token.create_access_token({'user': user.login, 'role': user.role})
            token_refresh = Token.create_refresh_token({"user": user.login, "role": user.role})
            await client.set(f'access:user:{user.login}', token_access, ex=3600)
            await client.set(f'refresh:user:{user.login}', token_refresh, ex=3600)
            await add_token(user.login, token_access, session)


            access = await client.get(f'access:user:{user.login}')
            refresh = await client.get(f'refresh:user:{user.login}')

            return {
                "message": f"{message}",
                "access_token": access.decode('utf-8'),
                "refresh_token": refresh.decode('utf-8')
            }
        except Exception as e:
            raise e
            #return {"message": f"An error occurred: {e}"}
