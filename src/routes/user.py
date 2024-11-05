from fastapi import APIRouter
from src.models import User_py

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.put("/")
def put_user(usr: User_py):
    pass

@user_router.delete("/")
def delete_user(usr: User_py):
    pass