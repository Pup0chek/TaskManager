from fastapi import APIRouter, Header, HTTPException
#from starlette import status

#from database.actions.with_token import add_token
from src.models import User_py
from database.connect_to_db import async_session
from database.actions.with_user import update_user, select_user, login, get_role_by_login, delete_user
from src.Token import Token

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.put("/")
async def put_user(user: User_py):
    async with async_session() as session:
        try:
            success = await update_user(user.login, user.password, user.role, session)
            if success:
                return {"message": "User updated successfully."}
            else:
                return {"message": f"User with login '{user.login}' not found."}
        except Exception as e:
            return {"message": f"An error occurred: {e}"}


@user_router.delete("/")
async def delete_user_endpoint(user: str, Authorization: str = Header(None)):
    async with async_session() as session:
        try:
            if not Authorization:
                raise HTTPException(status_code=401, detail="Authorization header is missing.")

            token = Authorization[7:] if Authorization.startswith("Bearer ") else Authorization
            payload = Token.decode_token(token)
            user1 = payload.get("user")

            role = await get_role_by_login(user1, session)
            if role != "admin":
                raise HTTPException(status_code=403, detail="You don't have permission for this action.")

            deleted_user = await delete_user(user, session)
            return {"message": "User deleted successfully.", "user": f"{deleted_user}"}
        except HTTPException as e:
            raise e
        except Exception as e:
            return {"message": f"An error occurred: {e}"}
