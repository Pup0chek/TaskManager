from fastapi import APIRouter
from src.models import User_py
from database.connect_to_db import Session
from database.actions.with_user import update_user

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
def delete_user(usr: User_py):
    pass