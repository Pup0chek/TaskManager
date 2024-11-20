from database.models import Task, User, Token_validation
from sqlalchemy import select

def add_token(user:str, token:str, session):
    try:
        statement = select(Token_validation).where(Token_validation.user == user)
        id1 = session.scalar(statement)

        # Проверяем, существует ли задача
        if not id1:
            token = Token_validation(user_id=id, jwt=token)
            return create_token(token, session)
        else:
            id.jwt = token
            session.commit()
            return {"message": "Token has been added"}
    except Exception as e:
        return {"message": f"{e}"}

def create_token(token:Token_validation, session):
    try:
        session.add(token)
        session.commit()
        session.refresh(token)
        return {"message": "Token created"}
    except Exception as e:
        session.rollback()
        return {"message": f"{e}"}