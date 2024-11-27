import jwt
from fastapi import HTTPException, Header
from datetime import datetime, timedelta
from database.actions.with_token import add_token


class Token:
    @staticmethod
    def create_access_token(data: dict, expiration_minutes: int = 60) -> str:
        expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
        data.update({"exp": expiration_time})
        token = jwt.encode(payload=data, key='hahahahhahaa')
        return token

    @staticmethod
    def decode_token(authorization: str):
        try:
            payload = jwt.decode(authorization, key='hahahahhahaa', algorithms=['HS256'])
            print(payload)
            #data = payload.get('user')
            return payload
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(
                status_code=401,
                detail=f"{e}"
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=401,
                detail=f"{e}"
            )
    @staticmethod
    def get_role(authorization:str):
        payload = jwt.decode(authorization, key='hahahahhahaa', algorithms=['HS256'])
        role= payload.get('role')
        return role

    @staticmethod
    def create_refresh_token(data:dict, expiration_days: int= 31) -> str:
        expiration_time = datetime.utcnow() + timedelta(days=expiration_days)
        data.update({"exp": expiration_time})
        token = jwt.encode(payload=data, key='hahahahhahaa')
        return token

    @staticmethod
    def refresh(token: str):
        try:
            payload = jwt.decode(token, 'hahahahhahaa', algorithms=['HS256'])
            username = payload.get("user")
            if username is None:
                raise HTTPException(status_code=403, detail="Could not validate credentials")
            new_access_token = Token.create_access_token(data={"user": username})
            return {"access_token": new_access_token}
        except Exception as e:
            raise HTTPException(status_code=403, detail=f"{e}")