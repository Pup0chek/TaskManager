from fastapi import APIRouter
from src.models import User_py
from database.models import User
from database.connect_to_db import select_user, Session

login_router = APIRouter(prefix='/login', tags=['Login'])

@login_router.get("/")
def get_registration():
    return {"message":"Welcome to login page!"}

@login_router.post("/")
def post_registration(user:User_py):
    with Session() as session:
        try:
            if select_user(user.login, session):
                return {"message": "success"}
        except Exception as e:
            return {"message": f"error: {e}"}