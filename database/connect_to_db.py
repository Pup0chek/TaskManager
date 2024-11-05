from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Task, User
from sqlalchemy import select

engine = create_engine('sqlite:///C:/TaskManager/database.db')

Session = sessionmaker(engine)

def create_task(task: Task, session) -> None:
    session.add(task)

def update_task(new_object: Task, session) -> None:
    session.merge(new_object)

def delete_task(name: str, session) -> Task:
    statement = select(Task).where(Task.name == name)
    db_objects = session.scalars(statement).all()

    for db_object in db_objects:
        session.delete(db_object)
    return db_object
def select_task(name: str, session) -> list[Task]:
    statement = select(Task).where(Task.name == name)
    db_objects = session.scalars(statement).all()
    return db_objects


