
from fastapi import APIRouter, Header, HTTPException


from src.models import Task_py
from database.models import Task
from src.Token import Token
from database.connect_to_db import Session
from database.actions.with_task import select_task_bool, select_task, create_task, update_task, owner

task_router = APIRouter(prefix='/task', tags=['Task'])

class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 401):
        super().__init__(status_code=status_code, detail=detail)


@task_router.get("/{id}")
async def get_by_id(id: int, authorization:str = Header(None)):
    if authorization is None:
        raise CustomException(status_code=401, detail="Where's your token?")
    with Session() as session:
        try:
            if authorization.startswith("Bearer "):
                token = authorization[7:]
            payload = Token.decode_token(token)
            owner1 = payload.get("user")
            try:
                if owner(id, owner1, session):
                    success = select_task(id, session)
                    if success:
                        return {
                            "id": f"{success.id}",
                            "name": f"{success.name}",
                            "description": f"{success.description}"
                        }
                    else:
                        return {"message": f"Task with name '{success[0]}' not found."}
                else:
                    raise HTTPException(
                        status_code=401,
                        detail=f"Permission denied"
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=401,
                    detail=f"{e}"
                )
        except Exception as e:
            raise e

@task_router.get("/")
async def get_task(limit: int=10):
    return {"message":"Welcome to task creation page"}

@task_router.post("/")
async def post_task(task:Task_py, authorization: str = Header(...)):
    with Session() as session:
        try:
            if authorization.startswith("Bearer "):
                token = authorization[7:]
            payload = Token.decode_token(token)
            owner = payload.get("user")
            print(payload)
            try:
                task1 = Task(name=task.name, description=task.description, owner=owner)
                create_task(task1, session)
                return {"message": "success"}
            except Exception as e:
                return {'message': f"error:{e}"}
        except HTTPException as e:
            raise e

@task_router.put("/")
async def put_task(task: Task_py):
    with Session() as session:
        try:
            # Используем обновлённую функцию для обновления задачи по имени и описанию
            success = update_task(task.name, task.description, session)
            if success:
                return {"message": "success"}
            else:
                return {"message": f"Task with name '{task.name}' not found."}
        except Exception as e:
            return {"message": f"error: {e}"}



@task_router.delete("/")
async def delete_task(task: Task_py):
    pass