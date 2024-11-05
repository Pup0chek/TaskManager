from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Task
from sqlalchemy import select

engine = create_engine('sqlite:///database.db')

Session = sessionmaker(engine)

def create_task(task: Task, session) -> None:
    session.add(task)
def update(new_object: Task, session) -> None:
    session.merge(new_object)

def get_by_name(name: str, session) -> list[Task]:
    statement = select(Task).where(Task.name == name)
    db_objects = session.scalars(statement).all()
    return db_objects


