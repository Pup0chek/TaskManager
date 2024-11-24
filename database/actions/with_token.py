from database.models import Task, User, Token_validation
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def add_token(user: str, token: str, session: AsyncSession):
    try:
        statement = select(Token_validation).where(Token_validation.user == user)
        token_entry = await session.scalar(statement)

        if not token_entry:
            new_token = Token_validation(user=user, jwt=token)
            await create_token(new_token, session)
            return {"message": "Token has been created"}
        else:
            token_entry.jwt = token
            await session.commit()
            return {"message": "Token has been updated"}
    except Exception as e:
        await session.rollback()
        return {"message": f"An error occurred: {e}"}


async def create_token(token: Token_validation, session: AsyncSession):
    try:
        session.add(token)
        await session.commit()
        await session.refresh(token)
        return {"message": "Token created"}
    except Exception as e:
        await session.rollback()
        return {"message": f"An error occurred while creating the token: {e}"}


async def valid_token(user: str, token: str, session: AsyncSession) -> bool:
    try:
        statement = select(Token_validation).where(Token_validation.user == user)
        token_entry = await session.scalar(statement)

        if not token_entry:
            return False

        return token_entry.jwt == token
    except Exception as e:
        print(f"An error occurred while validating the token: {e}")
        return False
