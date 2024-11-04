from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from items import router as items_router
from users.views import router as users_router
from core.config import create_tables, delete_tables

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")

app = FastAPI()
app.include_router(items_router)
app.include_router(users_router)

@app.get('/')
def get_root():
    return {"message": "Hi!!!!"}

@app.get('/hello')
def hello(name: str = "World"):
    name = name.strip().title() #убираем пробелы, а тайтл делаем большие первые буквы
    return {"message": f"Hello, {name}"}







if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)