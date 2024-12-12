from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database.models import Task, User, Base
from sqlalchemy import select

engine = create_async_engine('sqlite+aiosqlite:///./database.db', echo=True)
engine.echo = True

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



