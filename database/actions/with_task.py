from database.models import Task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_task(task: Task, session: AsyncSession) -> bool:
    try:
        session.add(task)
        await session.commit()
        await session.refresh(task)

        if task.id is not None:
            print(f"Task with ID {task.id} was successfully created.")
            return True
        else:
            print("Failed to create task: ID was not assigned.")
            return False
    except Exception as e:
        await session.rollback()
        print(f"An error occurred while creating task: {e}")
        return False






async def update_task(name: str, description: str, session: AsyncSession) -> bool:
    try:
        statement = select(Task).where(Task.name == name)
        task = await session.scalar(statement)

        if not task:
            print(f"Task with name '{name}' not found.")
            return False

        task.description = description
        task.name = name
        await session.commit()
        print(f"Task with name '{name}' was successfully updated.")
        return True
    except Exception as e:
        await session.rollback()
        print(f"An error occurred while updating task: {e}")
        return False


async def delete_task(id: int, session: AsyncSession) -> bool:
    try:
        statement = select(Task).where(Task.id == id)
        task = await session.scalar(statement)

        if not task:
            print(f"No tasks found with id: {id}")
            return False

        await session.delete(task)
        await session.commit()
        print(f"Tasks with id '{id}' have been deleted.")
        return True
    except Exception as e:
        await session.rollback()
        print(f"An error occurred while deleting tasks: {e}")
        return False


async def select_task_bool(name: str, session: AsyncSession) -> bool:
    try:
        statement = select(Task).where(Task.name == name)
        tasks = await session.scalars(statement)
        tasks = tasks.all()

        if not tasks:
            print(f"No tasks found with name: {name}")
            return True
        print(f"Tasks with this name ({name}) already exist")
        return False
    except Exception as e:
        print(f"An error occurred while selecting tasks: {e}")
        return False


async def select_task(id: int, session: AsyncSession) -> Task:
    try:
        statement = select(Task).where(Task.id == id)
        task = await session.scalar(statement)

        if not task:
            print(f"No task found with ID: {id}")
            return None

        return task
    except Exception as e:
        print(f"An error occurred while selecting task: {e}")
        return None


async def select_task_id(id: int, session: AsyncSession) -> bool:
    try:
        statement = select(Task).where(Task.id == id)
        task = await session.scalar(statement)

        if not task:
            print(f"No task found with ID: {id}")
            return False

        return True
    except Exception as e:
        print(f"An error occurred while selecting task: {e}")
        return False

async def owner(id: int, owner: str, session: AsyncSession) -> bool:
    try:
        statement = select(Task).where(Task.id == id)
        task = await session.scalar(statement)

        if not task:
            print(f"No task found with ID: {id}")
            return False

        return task.owner == owner
    except Exception as e:
        print(f"An error occurred while verifying owner: {e}")
        return False
