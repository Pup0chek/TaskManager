from tempfile import template

from celery.result import AsyncResult
from starlette.responses import JSONResponse

from src.worker import create_task, celery

import aioredis
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, Body
from fastapi.openapi.utils import get_openapi
from database.connect_to_db import async_session
from database.actions.with_token import add_token
from fastapi.templating import Jinja2Templates
from src.routes.registration import registration_router
from src.routes.login import login_router
from src.routes.task import task_router
from src.routes.user import user_router
from src.models import Refresh
from src.roles import role_required
from src.Token import Token

#from confluent_kafka import Producer

app = FastAPI()
app.include_router(registration_router)
app.include_router(login_router)
app.include_router(task_router)
app.include_router(user_router)

templates = Jinja2Templates(directory="templates")


producer_config = {
    'bootstrap.servers': 'localhost:9092',
    'security.protocol': 'PLAINTEXT'
}

# producer = Producer(producer_config)
#
# @app.post("/send")
# async def send_message(message: MessagePayload):
#     try:
#         producer.produce(message.topic, message.message)
#         producer.flush()
#         return {"status": "Message sent successfully"}
#     except Exception as e:
#         return {"status": "Error", "details": str(e)}


async def redis_client():
    return await aioredis.StrictRedis(host="localhost", port="6379", db=0)


@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    mail = payload["mail"]
    topic = payload["topic"]
    text = payload["text"]

    task = create_task.delay(mail, topic, text)
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id, app=celery)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)


@app.get('/main')
async def get_main(request: Request):
    template = templates.TemplateResponse('main.html', {"request":request})
    return template


@app.get('/admin')
async def get_admin(token: str = Depends(role_required('admin'))):
    return {"message": "This is the admin resource", "user": f'{token}'}


@app.get('/user')
async def get_user(token: str = Depends(role_required('user'))):
    return {"message": "This is the user resource", "user": f'{token}'}


@app.get('/guest')
async def get_guest(token: str = Depends(role_required('guest'))):
    return {"message": "This is the guest resource", "user": f'{token}'}


@app.post('/refresh')
async def post_refresh_token(token: Refresh, client=Depends(redis_client)):
    async with async_session() as session:
        try:
            access_token = Token.refresh(token.refresh_token)['access_token']
            payload = Token.decode_token(access_token).get('user')
            await add_token(payload, access_token, session)
            await client.set(f'access:user:{payload}', access_token)
            access = await client.get(f'access:user:{payload}')
            return {"message": "Token refreshed successfully", "token": f"{access.decode('utf-8')}"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error refreshing token: {e}")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom API with Authorization",
        version="1.0.0",
        description="This is a custom OpenAPI schema with Authorization support",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
