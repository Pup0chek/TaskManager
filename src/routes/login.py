from fastapi import APIRouter
from src.models import User_login
from database.connect_to_db import Session
from database.actions.with_token import add_token
from database.actions.with_user import select_user, login, get_role_by_login
from src.Token import Token

login_router = APIRouter(prefix='/login', tags=['Login'])

@login_router.get("/")
def get_login():
    return {"message":"Welcome to login page!"}

@login_router.post("/")
def post_login(user:User_login):
    with Session() as session:
        try:
            if select_user(user.login, session):
                if login(user.login, user.password, session):
                    role = get_role_by_login(user.login, session)
                    token_access = Token.create_access_token({"user": user.login, "role": role})
                    add_token(user.login, token_access, session)
                    token_refresh = Token.create_refresh_token({"user": user.login, "role": role})
                    return {"message": f"success", "access_token": f"{token_access}", "refresh_token": f"{token_refresh}"}
                else:
                    return {"message":"Password is incorrect"}
            return {"message": f"There's no user with login '{user.login}'. Try different one"}
        except Exception as e:
            return {"message": f"error: {e}"}

