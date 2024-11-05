import uvicorn
from fastapi import FastAPI
from routes.registration import registration_router
from routes.login import login_router
from routes.task import task_router

app = FastAPI()
app.include_router(registration_router)
app.include_router(login_router)
app.include_router(task_router)

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)