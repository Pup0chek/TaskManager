from fastapi import APIRouter
from src.models import Task_py
from database.models import Task
from database.connect_to_db import Session
from database.actions.with_task import select_task, create_task

task_router = APIRouter(prefix='/task', tags=['Task'])

@task_router.get("/")
def get_task():
    return {"message":"Welcome to task creation page"}

@task_router.post("/")
def post_task(task:Task_py):
    with Session() as session:
        try:
            if select_task(task.name, session):
                try:
                    task1 = Task(name=task.name, description=task.description)
                    create_task(task1, session)
                    return {"message": "success"}
                except Exception as e:
                    return {'message': f"error:{e}"}
        except:
            return {"message": f"Tasks with this name ({task.name}) already exist"}

@task_router.put("/")
def put_task(task: Task_py):
    pass

@task_router.delete("/")
def delete_task(task: Task_py):
    pass