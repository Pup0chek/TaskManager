from pydantic import BaseModel

class User(BaseModel):
    name: str
    password: str

class Task(BaseModel):
    name: str
    description:str
    tag: str