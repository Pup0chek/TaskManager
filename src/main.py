import uvicorn
from fastapi import FastAPI
from items import router as items_router
from users.views import router as users_router

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