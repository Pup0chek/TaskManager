from database.models import Token_validation
from sqlalchemy import select

def add_token(user:str, token:str, session):
    try:
        statement = select(Token_validation).where(Token_validation.user == user)
        id1 = session.scalar(statement)

        # Проверяем, существует ли задача
        if not id1:
            token = Token_validation(user= user, jwt=token)
            return create_token(token, session)
        else:
            id1.jwt = token
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

def valid_token(user:str, token:str, session) -> bool:
    statement = select(Token_validation).where(Token_validation.user == user)
    db_objects = session.scalars(statement).one()
    if db_objects.jwt == token:
        return True
    return False