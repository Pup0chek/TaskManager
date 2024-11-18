from fastapi import HTTPException, Depends, Header
from starlette import status
from src.Token import Token




def role_required(role: str):
    def role_checker(authorization: str = Header(...)):
        if authorization.startswith("Bearer "):
            token = authorization[7:]
        else:
            token = authorization
        payload = Token.decode_token(token)
        user_role = Token.get_role(token)
        if user_role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user_role
    return role_checker