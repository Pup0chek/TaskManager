from database.models import Task, User
from sqlalchemy import select


def create_user(user: User, session) -> None:
    try:

        session.add(user)
        session.commit()
        session.refresh(user)

        if user.id is not None:
            print(f"User with ID {user.id} was successfully created.")
            return True
        else:
            print("Failed to create user: ID was not assigned.")
            return False

    except Exception as e:
        session.rollback()
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