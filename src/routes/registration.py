from fastapi import APIRouter
from src.models import User_py
from database.models import User
from database.connect_to_db import  Session
from database.actions.with_user import create_user


registration_router = APIRouter(prefix='/registration', tags=['Registration'])

@registration_router.get("/")
def get_registration():
    return {"message":"Welcome to registration page!"}

@registration_router.post("/")
def post_registration(user:User_py):
    user1 = User(login=user.login, password=user.password)
    with Session() as session:
        try:
            create_user(user1, session)
            return {"message": "success"}
        except:
            return {"message": "error"}


