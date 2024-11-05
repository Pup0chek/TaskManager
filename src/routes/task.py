from fastapi import APIRouter
from src.models import Task_py

task_router = APIRouter(prefix='/task', tags=['Task'])

@task_router.get("/")
def get_registration():
    pass

@task_router.post("/")
def post_registration(task:Task_py):
    pass