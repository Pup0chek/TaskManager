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