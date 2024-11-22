from database.models import Task, User
from sqlalchemy import select


def create_user(user: User, session) -> None:
    try:
        session.add(user)
        session.commit()
        session.refresh(user)

        if user.id is not None:
            return f"User with ID {user.id} was successfully created."
        else:
            return "Failed to create user: ID was not assigned."

    except Exception as e:
        session.rollback()
        return f"An error occurred while creating user: {e}"


def update_user(login: str, password: str, session) -> bool:
    try:
        # Ищем задачу по имени
        statement = select(User).where(User.login == login)
        task = session.scalar(statement)

        # Проверяем, существует ли задача
        if not task:
            print(f"Task with name '{login}' not found.")
            return False

        # Обновляем поля задачи
        task.password = password
        # Можно добавить другие поля для обновления здесь при необходимости

        session.commit()
        print(f"Task with name '{login}' was successfully updated.")
        return True
    except Exception as e:
        session.rollback()
        print(f"An error occurred while updating task: {e}")
        return False

def delete_user(login: str, session) -> Task:
    statement = select(User).where(User.login == login)
    db_objects = session.scalars(statement).one()

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
def login(login:str, password:str, session) -> bool:
    user = session.execute(select(User).where(User.login == login)).scalar_one_or_none()
    if password == user.password:
        return True
    return False

def get_role_by_login(login:str, session) -> str:
    role = session.execute(select(User).where(User.login == login)).scalar_one_or_none()
    return role.role