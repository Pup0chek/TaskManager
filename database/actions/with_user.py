from database.models import Task, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(user: User, session: AsyncSession) -> str:
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)

        if user.id is not None:
            return f"User with ID {user.id} was successfully created."
        else:
            return "Failed to create user: ID was not assigned."

    except Exception as e:
        await session.rollback()
        return f"An error occurred while creating user: {e}"


async def update_user(login: str, password: str, role:str, session: AsyncSession) -> bool:
    try:
        statement = select(User).where(User.login == login)
        user = await session.scalar(statement)
        if not user:
            print(f"User with login '{login}' not found.")
            return False

        user.login = login
        user.password = password
        user.role = role

        await session.commit()
        print(f"User with login '{login}' was successfully updated.")
        return True
    except Exception as e:
        await session.rollback()
        print(f"An error occurred while updating user: {e}")
        return False


async def delete_user(login: str, session: AsyncSession) -> User:
    try:
        statement = select(User).where(User.login == login)
        user = await session.scalar(statement)

        if not user:
            raise ValueError(f"No user found with login: {login}")

        await session.delete(user)
        await session.commit()
        return user
    except Exception as e:
        await session.rollback()
        raise ValueError(f"An error occurred while deleting user: {e}")


async def select_user(login: str, session: AsyncSession) -> User:
    try:
        statement = select(User).where(User.login == login)
        user = await session.scalar(statement)

        if not user:
            print(f"No user found with login: {login}")
            return None

        print(user)
        return user
    except Exception as e:
        print(f"An error occurred while selecting user: {e}")
        return None


async def login(login: str, password: str, session: AsyncSession) -> bool:
    try:
        statement = select(User).where(User.login == login)
        user = await session.scalar(statement)

        if not user:
            print(f"No user found with login: {login}")
            return False

        if password == user.password:
            return True
        else:
            print("Incorrect password.")
            return False
    except Exception as e:
        print(f"An error occurred while logging in: {e}")
        return False


async def get_role_by_login(login: str, session: AsyncSession) -> str:
    try:
        statement = select(User).where(User.login == login)
        user = await session.scalar(statement)

        if not user:
            raise ValueError(f"No user found with login: {login}")

        return user.role
    except Exception as e:
        print(f"An error occurred while getting user role: {e}")
        return None
