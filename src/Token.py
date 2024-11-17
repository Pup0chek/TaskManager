import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta


class Token:
    @staticmethod
    def create_token(data: dict, expiration_minutes: int = 60):
        expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)

        # Добавляем 'exp' в payload, чтобы указать время жизни токена
        data.update({"exp": expiration_time})
        token = jwt.encode(payload=data, key='hahahahhahaa')
        return token

    @staticmethod
    def decode_token(token: str):
        try:

            payload = jwt.decode(token, key='hahahahhahaa')
            print(payload)
            data = payload.get('user')
            print(data)
            return data
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token error"
            )
