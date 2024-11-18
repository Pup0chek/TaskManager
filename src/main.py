import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends

from routes.registration import registration_router
from routes.login import login_router
from routes.task import task_router
from routes.user import user_router
from src.models import User_login
from src.roles import role_required

app = FastAPI()
app.include_router(registration_router)
app.include_router(login_router)
app.include_router(task_router)
app.include_router(user_router)


#course

@app.get('/admin')
def get_admin(token:str = Depends(role_required('admin'))):
    return {"message": "This is the admin resource", "user": f'{token}'}

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)