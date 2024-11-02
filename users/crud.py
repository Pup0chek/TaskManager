from users.schemas import CreateUser

def create_user(user_in) -> dict:
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user_in["username"],
    }