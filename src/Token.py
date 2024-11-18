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

            payload = jwt.decode(token, key='hahahahhahaa', algorithms=['HS256'])
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
