import uvicorn
from fastapi import FastAPI, Header
from fastapi.params import Depends

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
    try:
        return Token.refresh(token.refresh_token)
    except Exception as e:
        raise e


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)