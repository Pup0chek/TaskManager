from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Task, User, Base
from sqlalchemy import select

engine = create_engine('sqlite:///C:/TaskManager/database.db')

Session = sessionmaker(engine)


def create_db_and_tables() -> None:
	Base.metadata.create_all(engine)
def create_task(task: Task, session) -> None:
    try:
        # Добавляем объект в сессию
        session.add(task)
        session.commit()  # Коммитим изменения в базу данных
        session.refresh(task)  # Обновляем объект из базы данных

        # Проверяем, был ли объект сохранён в базе данных (по наличию ID, например)
        if task.id is not None:
            print(f"Task with ID {task.id} was successfully created.")
            return True
        else:
            print("Failed to create task: ID was not assigned.")
            return False

    except Exception as e:
        session.rollback()  # Откатываем транзакцию при ошибке
        print(f"An error occurred while creating user: {e}")
        return False

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
    if not db_objects:
        print(f"No tasks found with login: {name}")
        return True
    print(f"Tasks with this name ({name}) already exist")
    return False
#------------------------------------------------------------
def create_user(user: User, session) -> None:
    try:
        # Добавляем объект в сессию
        session.add(user)
        session.commit()  # Коммитим изменения в базу данных
        session.refresh(user)  # Обновляем объект из базы данных

        # Проверяем, был ли объект сохранён в базе данных (по наличию ID, например)
        if user.id is not None:
            print(f"User with ID {user.id} was successfully created.")
            return True
        else:
            print("Failed to create user: ID was not assigned.")
            return False

    except Exception as e:
        session.rollback()  # Откатываем транзакцию при ошибке
        print(f"An error occurred while creating user: {e}")
        return False

def update_user(new_object: User, session) -> None:
    session.merge(new_object)

def delete_user(login: str, session) -> Task:
    statement = select(login).where(User.login == login)
    db_objects = session.scalars(statement).all()

    for db_object in db_objects:
        session.delete(db_object)
    return db_object

def select_user(login: str, session) -> list[User]:
    statement = select(User).where(User.login == login)
    db_objects = session.scalars(statement).all()
    if not db_objects:
        print(f"No user found with login: {login}")
        return False
    print(db_objects)
    return True
