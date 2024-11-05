from fastapi import APIRouter
from src.models import User_py

login_router = APIRouter(prefix='/login', tags=['Login'])

@login_router.get("/")
def get_registration():
    pass

@login_router.post("/")
def post_registration(user:User_py):
    pass