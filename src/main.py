import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.params import Depends
from database.connect_to_db import Session
from database.actions.with_token import add_token

from src.routes.registration import registration_router
from src.routes.login import login_router
from src.routes.task import task_router
from src.routes.user import user_router
from src.models import Refresh
from src.roles import role_required
from src.Token import Token

app = FastAPI()
app.include_router(registration_router)
app.include_router(login_router)
app.include_router(task_router)
app.include_router(user_router)



#course

@app.get('/admin')
def get_admin(token:str = Depends(role_required('admin'))):
    return {"message": "This is the admin resource", "user": f'{token}'}

@app.get('/user')
def get_user(token:str = Depends(role_required('user'))):
    return {"message": "This is the user resource", "user": f'{token}'}

@app.get('/guest')
def get_user(token: str = Depends(role_required('guest'))):
    return {"message": "This is the guest resource", "user": f'{token}'}

@app.post('/refresh')
def post_refresh_token(token:Refresh):
    with Session() as session:
        try:
            token = Token.refresh(token.refresh_token)['access_token']
            payload = Token.decode_token(token).get('user')
            add_token(payload, token, session)
            return {"message":"refreshed"}
        except Exception as e:
            raise e

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

# Подключаем кастомное OpenAPI к приложению
app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)