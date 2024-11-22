from fastapi import APIRouter, Header

from database.actions.with_token import add_token
from src.models import User_py
from database.connect_to_db import Session
from database.actions.with_user import update_user, select_user, login, get_role_by_login
from src.Token import Token


user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.put("/")
def put_user(user: User_py):
    with Session() as session:
        try:
            # Используем обновлённую функцию для обновления задачи по имени и описанию
            success = update_user(user.login, user.password, session)
            if success:
                return {"message": "success"}
            else:
                return {"message": f"Task with name '{user.login}' not found."}
        except Exception as e:
            return {"message": f"error: {e}"}

@user_router.delete("/")
def delete_user(user: str, Authorization: str = Header(...)):
    with Session() as session:
        try:
            if Authorization.startswith("Bearer "):
                token = Authorization[7:]
            payload = Token.decode_token(token)
            user1 = payload.get("user")
            role = get_role_by_login(user1, session)
            print('--------------'+role+'-------------------')
            if role == "admin":
                u = delete_user(user, session)
                return {"message": "User deleted", "user":f"{u}"}
            return {"message": "You don't have permission for this action."}

        except Exception as e:
            return {"message": f"error: {e}"}
