import jwt

class Token:
    @staticmethod
    def create_token(data: dict):
        token = jwt.encode(payload=data, key='hahahahhahaa')
        return token

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, key='hahahahhahaa')
            data = payload.get('login')
            return data
        except jwt.ExpiredSignatureError:
            return {"message": "ExpiredSignatureError"}
        except jwt.InvalidTokenError:
            return {"message": "InvalidTokenError"}
