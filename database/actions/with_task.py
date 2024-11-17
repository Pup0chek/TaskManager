from database.models import Task
from sqlalchemy import select



def create_task(task: Task, session) -> None:
    try:

        session.add(task)
        session.commit()
        session.refresh(task)

        if task.id is not None:
            print(f"Task with ID {task.id} was successfully created.")
            return True
        else:
            print("Failed to create task: ID was not assigned.")
            return False

    except Exception as e:
        session.rollback()
        print(f"An error occurred while creating user: {e}")
        return False

def update_task(name: str, description: str, session) -> bool:
    try:
        # Ищем задачу по имени
        statement = select(Task).where(Task.name == name)
        task = session.scalar(statement)

        # Проверяем, существует ли задача
        if not task:
            print(f"Task with name '{name}' not found.")
            return False

        # Обновляем поля задачи
        task.description = description
        # Можно добавить другие поля для обновления здесь при необходимости

        session.commit()
        print(f"Task with name '{name}' was successfully updated.")
        return True
    except Exception as e:
        session.rollback()
        print(f"An error occurred while updating task: {e}")
        return False

def delete_task(name: str, session) -> Task:
    statement = select(Task).where(Task.name == name)
    db_objects = session.scalars(statement).all()

    for db_object in db_objects:
        session.delete(db_object)
    return db_object

def select_task_bool(name: str, session) -> list[Task]:
    statement = select(Task).where(Task.name == name)
    db_objects = session.scalars(statement).all()
    if not db_objects:
        print(f"No tasks found with name: {name}")
        return True
    print(f"Tasks with this name ({name}) already exist")
    return False

def select_task(id: int, session) -> list[Task]:
    statement = select(Task).where(Task.id == id)
    db_objects = session.scalars(statement).one()
    return db_objects