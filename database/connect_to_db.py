from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Task, User, Base
from sqlalchemy import select

engine = create_engine('sqlite:///C:/TaskManager/database.db')
engine.echo = True

Session = sessionmaker(engine)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)



