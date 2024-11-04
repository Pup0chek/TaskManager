from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from models.task import Base_model, Task

engine = create_async_engine("sqlite+aiosqlite:///database.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_async(Base_model.metadata.create_all)
async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_async(Base_model.metadata.drop_all())