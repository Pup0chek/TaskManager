from pydantic import BaseModel

class User_py(BaseModel):
    login: str
    password: str
    role: str

class MessagePayload(BaseModel):
    topic: str
    message: str

class User_login(BaseModel):
    login: str
    password: str

class Task_py(BaseModel):
    name: str
    description:str

class Refresh(BaseModel):
    refresh_token: str