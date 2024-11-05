from fastapi import APIRouter
from src.models import User

registration_router = APIRouter(prefix='/registration', tags='Registration')

@registration_router.get("/")
def get_registration():
    pass

@registration_router.post("/")
def post_registration(user:User):
    pass