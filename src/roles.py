from fastapi import HTTPException, Depends, Header
from starlette import status
from src.Token import Token


from src.models import User_login


def role_required(role: str):
    def role_checker(authorization: str = Header(...)):
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token prefix")

        token = authorization[7:]
        user_role = Token.get_role(token)
        if user_role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user_role

    return role_checker